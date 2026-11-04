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
    
    const n_FF = tf.image.resizeNearestNeighbor(tensor, [224, 224], false, false).cast('float32').div(255.0).expandDims(0);
    const n_TF = tf.image.resizeNearestNeighbor(tensor, [224, 224], true, false).cast('float32').div(255.0).expandDims(0);
    const n_FT = tf.image.resizeNearestNeighbor(tensor, [224, 224], false, true).cast('float32').div(255.0).expandDims(0);
    
    const b_FF = tf.image.resizeBilinear(tensor, [224, 224], false, false).cast('float32').div(255.0).expandDims(0);
    const b_TF = tf.image.resizeBilinear(tensor, [224, 224], true, false).cast('float32').div(255.0).expandDims(0);
    const b_FT = tf.image.resizeBilinear(tensor, [224, 224], false, true).cast('float32').div(255.0).expandDims(0);

    return {
      n_FF: Array.from(n_FF.dataSync()),
      n_TF: Array.from(n_TF.dataSync()),
      n_FT: Array.from(n_FT.dataSync()),
      b_FF: Array.from(b_FF.dataSync()),
      b_TF: Array.from(b_TF.dataSync()),
      b_FT: Array.from(b_FT.dataSync())
    };
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\js_resize_variants.json', JSON.stringify(result));
  console.log("JS resize variants saved.");
  
  await browser.close();
})();
