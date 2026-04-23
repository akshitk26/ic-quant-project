import fs from 'fs/promises';
import path from 'path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const base = '/Users/akshit/Code/IC Quant Project';
const outputDir = path.join(base, 'outputs', 'defense_slide');
const scratchDir = path.join(base, 'tmp', 'slides', 'defense_slide');
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(scratchDir, { recursive: true });

const deckPath = path.join(outputDir, 'defense_vs_tech_one_slide.pptx');
const previewPath = path.join(scratchDir, 'defense_vs_tech_one_slide.png');

const imgBiased = `data:image/png;base64,${Buffer.from(await fs.readFile(path.join(base, 'outputs', 'defense_biased_regime_strategy.png'))).toString('base64')}`;
const imgLagged = `data:image/png;base64,${Buffer.from(await fs.readFile(path.join(base, 'outputs', 'defense_lagged_regime_strategy.png'))).toString('base64')}`;

const C = {
  bg: '#F6F3EE',
  text: '#18212B',
  muted: '#5E6874',
  white: '#FFFDF9',
  blue: '#315BFF',
  green: '#2D7A5F',
  red: '#A34131',
  sand: '#ECE2D4',
};

const pres = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = pres.slides.add();
slide.background.fill = C.bg;

function textBox({ x, y, w, h, text, size, color = C.text, bold = false, fill = C.bg, align = 'left' }) {
  const shape = slide.shapes.add({ geometry: 'rect', x, y, width: w, height: h, fill });
  shape.position = { left: x, top: y, width: w, height: h };
  shape.text.set(text);
  shape.text.fontSize = size;
  shape.text.color = color;
  shape.text.bold = bold;
  shape.text.wrap = true;
  shape.text.alignment = align;
  shape.text.verticalAlignment = 'middle';
  shape.text.insets = { left: 6, right: 6, top: 2, bottom: 2 };
  return shape;
}

function card({ x, y, w, h, title, badge, badgeColor, imageDataUrl }) {
  const bg = slide.shapes.add({ geometry: 'rect', x, y, width: w, height: h, fill: C.white });
  bg.position = { left: x, top: y, width: w, height: h };
  textBox({ x: x + 18, y: y + 10, w: 230, h: 26, text: title, size: 20, bold: true, fill: C.white });
  textBox({ x: x + w - 158, y: y + 10, w: 136, h: 24, text: badge, size: 11, bold: true, color: '#FFFFFF', fill: badgeColor, align: 'center' });
  const img = slide.images.add({ dataUrl: imageDataUrl, alt: title });
  img.position = { left: x + 16, top: y + 46, width: w - 32, height: 278 };
  img.fit = 'contain';
}

textBox({ x: 64, y: 34, w: 220, h: 20, text: 'DEFENSE VS TECH', size: 11, color: C.blue, bold: true });
textBox({ x: 64, y: 54, w: 920, h: 58, text: 'the most interesting result was how the strategy changed once the backtest became realistic', size: 27, bold: true });
textBox({ x: 64, y: 112, w: 720, h: 24, text: 'same idea  same market  different implementation  different conclusion', size: 14, color: C.muted });

card({ x: 64, y: 162, w: 560, h: 332, title: 'biased regime strategy', badge: 'false positive', badgeColor: C.red, imageDataUrl: imgBiased });
card({ x: 656, y: 162, w: 560, h: 332, title: 'lagged regime strategy', badge: 'corrected test', badgeColor: C.green, imageDataUrl: imgLagged });

const panel = slide.shapes.add({ geometry: 'rect', x: 64, y: 528, width: 1152, height: 122, fill: C.sand });
panel.position = { left: 64, top: 528, width: 1152, height: 122 };
textBox({ x: 86, y: 544, w: 130, h: 18, text: 'KEY FINDING', size: 11, color: C.blue, bold: true, fill: C.sand });
textBox({ x: 86, y: 564, w: 1090, h: 34, text: 'the original chart looked strong because it used same day information  once the signal was delayed by one trading day most of the edge disappeared', size: 19, bold: true, fill: C.sand });
textBox({ x: 86, y: 604, w: 1090, h: 18, text: 'implication  intuitive rotation rules can look convincing in charts but fail once the test is implemented correctly', size: 13, color: C.muted, fill: C.sand });

const pptx = await PresentationFile.exportPptx(pres);
await fs.writeFile(deckPath, Buffer.from(pptx.data));
const pngBlob = await pres.export({ slide, format: 'png', scale: 1 });
await fs.writeFile(previewPath, Buffer.from(await pngBlob.arrayBuffer()));
console.log(JSON.stringify({ deckPath, previewPath }, null, 2));
