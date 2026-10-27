const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://localhost:8000');await page.waitForFunction(()=>document.querySelector('#count').textContent!=='—');const baseline=await (await page.request.get('http://localhost:8000/api/orders')).json();if(baseline.length!==3||baseline.some(o=>o.status!=='created'))throw Error('Capture requires a fresh three-order demonstration database.');
 const dir=require('path').join(__dirname,'../assets/screenshots/');require('fs').mkdirSync(dir,{recursive:true});
 await page.screenshot({path:dir+'SS1_Aerospace_Overview.png',fullPage:true});
 const row=page.locator('#rows tr').filter({hasText:'Northstar Components'});
 for(const action of ['approve','deliver','verify']){await row.getByRole('button',{name:action,exact:true}).click();await page.waitForFunction(()=>document.querySelector('#rows').textContent.includes('Northstar'));await page.waitForTimeout(120);}
 const second=page.locator('#rows tr').filter({hasText:'Aero Precision'});await second.getByRole('button',{name:'approve',exact:true}).click();
 await page.waitForFunction(()=>document.querySelector('#verified').textContent==='1');
 await page.screenshot({path:dir+'SS2_Aerospace_Workflow.png',fullPage:true});
 page.on('dialog',async dialog=>{console.log('Audit dialog:',dialog.message());await dialog.dismiss();});
 await row.getByRole('button',{name:'Audit',exact:true}).click();
 const result=await page.request.get('http://localhost:8000/api/orders/1/verify');const audit=await result.json();
 if(!audit.valid||audit.events!==4)throw Error('Audit failed');
 // Browser-native alert dialogs are not included in Chromium screenshots.
 // Capture the actual JSON endpoint result directly in the browser instead.
 await page.goto('http://localhost:8000/api/orders/1/verify');
 await page.screenshot({path:dir+'SS3_Aerospace_Audit.png',fullPage:true});
 console.log(JSON.stringify({browserErrors:errors,audit}));
 await browser.close();
})().catch(error=>{console.error(error.message);process.exit(1)});
