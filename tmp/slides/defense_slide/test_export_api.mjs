const { Presentation, PresentationFile } = await import('@oai/artifact-tool');
const pres = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = pres.slides.add();
slide.shapes.add({ geometry: 'rect', x: 10, y: 10, width: 100, height: 50, fill: '#ff0000' });
console.log('export_type', typeof pres.export);
console.log('slide_export_type', typeof slide.export);
try {
  const png = await pres.export({ format: 'png', slide });
  console.log('png', typeof png, Object.keys(png || {}).slice(0,10));
} catch (e) {
  console.log('png_err', e.message);
}
try {
  const out = await PresentationFile.exportPptx(pres);
  console.log('pptx_type', typeof out, Object.keys(out || {}).slice(0,10));
} catch (e) {
  console.log('pptx_err', e.message);
}
