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
    const img = new Image();
    img.src = dataUrl;
    await new Promise(r => { img.onload = r; });
    
    let tensor = tf.browser.fromPixels(img);
    let tensorNearest = tf.image.resizeNearestNeighbor(tensor, [224, 224]);
    let jsTensor = tf.cast(tensorNearest, 'float32').div(255.0);
    // expand dims like python
    jsTensor = jsTensor.expandDims(0);

    return {
      shape: jsTensor.shape,
      dtype: jsTensor.dtype,
      min: jsTensor.min().dataSync()[0],
      max: jsTensor.max().dataSync()[0],
      mean: jsTensor.mean().dataSync()[0],
      values: Array.from(jsTensor.dataSync())
    };
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\js_input.json', JSON.stringify(result));
  console.log("JS input tensor saved.");
  
  await browser.close();
})();
