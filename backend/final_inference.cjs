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
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/tf-tflite.min.js' });

  const imageBase64 = fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg').toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const pyData = JSON.parse(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_python_tensor.json'));
  
  const result = await page.evaluate(async (dataUrl, pyDataObj) => {
    tflite.setWasmPath('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/');
    
    // Simulate loading model over fetch since local fetch might fail in file://
    // So we'll pass the model as arrayBuffer
    return new Promise(resolve => {
        window.resolveTest = resolve;
    });
  }, dataUrl, pyData);
  
  await browser.close();
})();
