const { Presentation } = await import('@oai/artifact-tool');
function protoKeys(obj) {
  const out = new Set(); let p=obj; while (p){ for (const k of Object.getOwnPropertyNames(p)) out.add(k); p=Object.getPrototypeOf(p);} return [...out].sort();
}
const pres = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = pres.slides.add();
const image = slide.images.add({ uri: '/Users/akshit/Code/IC Quant Project/outputs/defense_biased_regime_strategy.png', alt: 'chart' });
console.log('image_proto_keys', protoKeys(image));
console.log('image_position_before', image.position);
image.position = { left: 10, top: 10, width: 400, height: 200 };
console.log('image_position_after', image.position);
