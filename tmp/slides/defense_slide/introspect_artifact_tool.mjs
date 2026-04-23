const { Presentation, PresentationFile } = await import('@oai/artifact-tool');
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
console.log('presentation_proto_keys', protoKeys(pres));
console.log('slides_proto_keys', protoKeys(pres.slides));
console.log('slide_proto_keys', protoKeys(slide));
console.log('shapes_proto_keys', protoKeys(slide.shapes));
console.log('images_proto_keys', protoKeys(slide.images));
console.log('charts_proto_keys', protoKeys(slide.charts));
console.log('presentationfile_proto_keys', protoKeys(PresentationFile));
