// Optional Node.js smoke test: execute the real template script with DOM doubles.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const template = fs.readFileSync(path.join(__dirname, '../assets/preview-template.html'), 'utf8');
const script = template.match(/<script>([\s\S]*?)<\/script>/)[1];

async function scenario(secure, writeSucceeds, fallbackSucceeds) {
  let copied, fallbackCalls = 0, selected = false, selectedElement;
  const article = {innerHTML: '<section><span leaf="">正文</span></section>', innerText: '正文'};
  const button = {disabled: false, textContent: '复制'};
  const toast = {textContent: '', classList: {add() {}, remove() {}}};
  const selection = {removeAllRanges() {selected = false;}, addRange() {selected = true;}};
  const context = {
    Blob, window: {isSecureContext: secure, getSelection: () => selection, ClipboardItem: true},
    ClipboardItem: class {constructor(payload) {this.payload = payload;}},
    navigator: {clipboard: {async write(items) {if (!writeSucceeds) throw Error('denied'); copied = items[0].payload;}}},
    document: {
      getElementById(id) {return {'gzh-content': article, gzhCopyBtn: button, gzhToast: toast}[id];},
      createRange() {return {selectNodeContents(el) {selectedElement = el;}};},
      execCommand(command) {assert.equal(command, 'copy'); assert.equal(selected, true); fallbackCalls++; return fallbackSucceeds;}
    },
    setTimeout() {return 1;}, clearTimeout() {}
  };
  vm.createContext(context);
  vm.runInContext(script, context);
  await context.gzhCopy();
  assert.equal(button.disabled, false);
  if (secure && writeSucceeds) {
    assert.equal(await copied['text/html'].text(), article.innerHTML);
    assert.equal(await copied['text/plain'].text(), article.innerText);
    assert.equal(fallbackCalls, 0);
    assert.equal(selected, false);
  } else {
    assert.equal(fallbackCalls, 1);
    assert.equal(selectedElement, article);
    assert.equal(selected, !fallbackSucceeds);
    if (!fallbackSucceeds) assert.match(toast.textContent, /Ctrl\/⌘\+C/);
  }
}

(async () => {
  await scenario(true, true, false);
  await scenario(true, false, true);
  await scenario(false, false, true);
  await scenario(false, false, false);
  console.log('Clipboard smoke tests: 4 passed');
})().catch(error => {console.error(error); process.exitCode = 1;});
