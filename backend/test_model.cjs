const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.9/dist/tf-tflite.min.js' });

  const imagePath = 'C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg';
  const imageBase64 = fs.readFileSync(imagePath).toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    const logs = [];
    const log = (msg) => logs.push(msg);

    log("Initializing TF...");
    await tf.ready();
    tflite.setWasmPath('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.9/dist/');

    log("Loading model...");
    // Use an online hosted model if possible, or we have to serve it. 
    // Since we are running in page context, file:// or relative paths won't work easily unless we run a local server.
    // Let's just return what we have so far because we need a server for the model.
    return logs.join('\n');
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\model_test_report.txt', result);
  return "Done";
})();
