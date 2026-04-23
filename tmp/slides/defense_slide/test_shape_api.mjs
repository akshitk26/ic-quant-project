const { Presentation } = await import('@oai/artifact-tool');
function protoKeys(obj) {
  const out = new Set();
  let p = obj;
  while (p) {
    for (const k of Object.getOwnPropertyNames(p)) out.add(k);
    p = Object.getPrototypeOf(p);
  }
  return [...out].sort();
}
const pres = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = pres.slides.add();
const shape = slide.shapes.add({ geometry: 'rect', x: 10, y: 10, width: 100, height: 50, fill: '#ff0000' });
console.log('shape_proto_keys', protoKeys(shape));
console.log('shape_keys', Object.keys(shape));
console.log('shape_text_type', typeof shape.text, shape.text ? protoKeys(shape.text) : null);
