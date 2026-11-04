const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });

  const result = await page.evaluate(async () => {
    // create a 10x10 black image
    const canvas = document.createElement('canvas');
    canvas.width = 10;
    canvas.height = 10;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = 'red'; // [255, 0, 0]
    ctx.fillRect(0, 0, 10, 10);
    const img = new Image();
    img.src = canvas.toDataURL();
    await new Promise(r => { img.onload = r; });
    
    let tensor = tf.browser.fromPixels(img);
    const tensor2 = tf.image.resizeBilinear(tensor, [5, 5]);
    const tensor3 = tf.cast(tensor2, 'float32').div(255.0);
    const batched = tensor3.expandDims(0);
    
    return Array.from(batched.dataSync()).slice(0, 50);
  });
  
  console.log(result);
  await browser.close();
})();
