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

  const imageBase64 = fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg').toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    // 1. JS Preprocessing (Current Code)
    const img = new Image();
    img.src = dataUrl;
    await new Promise(r => { img.onload = r; });
    
    let tensor = tf.browser.fromPixels(img);
    let tensorBilinear = tf.image.resizeBilinear(tensor, [224, 224]);
    let jsTensor = tf.cast(tensorBilinear, 'float32').div(255.0);
    const batchedJs = jsTensor.expandDims(0);

    return {
      js_first_100: Array.from(jsTensor.dataSync()).slice(0, 100),
      js_shape: jsTensor.shape,
      js_dtype: jsTensor.dtype,
      js_min: jsTensor.min().dataSync()[0],
      js_max: jsTensor.max().dataSync()[0],
      js_mean: jsTensor.mean().dataSync()[0],
      js_full_tensor: Array.from(jsTensor.dataSync())
    };
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_js_results.json', JSON.stringify(result));
  console.log("JS tensor dump complete.");
  
  await browser.close();
})();
