const { chromium } = require('playwright');
const path = require('path');

async function capture() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 950 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

  const fileUrl = 'file:///' + path.resolve(__dirname, '../index.html').replace(/\\/g, '/');
  console.log('Loading:', fileUrl);
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const outDir = path.resolve(__dirname, '../docs/assets/screenshots');

  // 1. Overview screenshot (Hero + Header + Stats)
  console.log('Capturing 01-hub-overview.png...');
  await page.screenshot({ path: path.join(outDir, '01-hub-overview.png') });

  // 2. Scroll to skills grid
  console.log('Capturing 02-skills-catalog.png...');
  await page.evaluate(() => window.scrollTo(0, 560));
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '02-skills-catalog.png') });

  // 3. Search for creative / 3D tools
  console.log('Capturing 03-new-creative-skills.png...');
  await page.evaluate(() => window.scrollTo(0, 420));
  await page.fill('#search-input', 'vanta');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '03-new-creative-skills.png') });

  // 4. Open skill modal by clicking inspect button
  console.log('Capturing 04-skill-detail-modal.png...');
  const inspectBtn = page.locator('.btn-inspect-spec').first();
  if (await inspectBtn.isVisible()) {
    await inspectBtn.click();
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(outDir, '04-skill-detail-modal.png') });
    // Close modal
    await page.evaluate(() => window.closeModal('detail-modal'));
    await page.waitForTimeout(300);
  }

  // Clear search input
  await page.fill('#search-input', '');
  await page.waitForTimeout(400);

  // 5. Open Master Prompt Modal
  console.log('Capturing 05-master-prompt.png...');
  await page.evaluate(() => window.openMasterPromptModal());
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '05-master-prompt.png') });
  await page.evaluate(() => window.closeModal('master-prompt-modal'));
  await page.waitForTimeout(300);

  // 6. Open Planner Modal
  console.log('Capturing 06-custom-prompt-planner.png...');
  await page.evaluate(() => {
    // Select first two skills if none selected
    if (window.selectedSkillIds && window.selectedSkillIds.size === 0) {
      const skills = window.LAY_SKILLS || [];
      if (skills[0]) window.selectedSkillIds.add(skills[0].id);
      if (skills[1]) window.selectedSkillIds.add(skills[1].id);
      if (window.updateSelectionUI) window.updateSelectionUI();
    }
    window.openProjectPlannerModal();
  });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '06-custom-prompt-planner.png') });
  await page.evaluate(() => window.closeModal('planner-modal'));
  await page.waitForTimeout(300);

  // 7. High-impact Social / LinkedIn card (1200x630 @ 2x)
  console.log('Capturing 07-social-linkedin-card.png...');
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, '07-social-linkedin-card.png') });

  await browser.close();
  console.log('[OK] All screenshots captured successfully in docs/assets/screenshots/');
}

capture().catch(err => {
  console.error('Error during capture:', err);
  process.exit(1);
});
