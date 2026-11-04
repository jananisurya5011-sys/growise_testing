const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  const logs = [];
  page.on('console', msg => logs.push(msg.text()));

  try {
    await page.goto('http://localhost:5173/ml', { waitUntil: 'networkidle0' });
    
    // Wait for initialization to finish
    await new Promise(r => setTimeout(r, 2000));
    
    // Upload file
    const fileInput = await page.$('input[type="file"]');
    await fileInput.uploadFile('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg');
    
    // Wait a bit
    await new Promise(r => setTimeout(r, 500));
    
    // Click Analyze
    const buttons = await page.$$('button');
    let analyzeBtn;
    for (const btn of buttons) {
      const text = await page.evaluate(el => el.textContent, btn);
      if (text.includes('Analyze Leaf')) {
        analyzeBtn = btn;
        break;
      }
    }
    
    if (analyzeBtn) {
      await analyzeBtn.click();
      await new Promise(r => setTimeout(r, 2000));
      
      await analyzeBtn.click();
      await new Promise(r => setTimeout(r, 2000));
    }
  } catch(e) {
    logs.push("Error: " + e.message);
  }
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\real_app_trace.txt', logs.join('\n'));
  await browser.close();
  return "Done";
})();
