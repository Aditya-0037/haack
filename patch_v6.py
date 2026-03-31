import codecs

with codecs.open('c:/Users/upadh/haack/index.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Remove previous CSS Background grid and orbs
css_start = html.find('/* Animated Background Grid */')
css_end = html.find('/* UI Components */')
if css_start != -1 and css_end != -1:
    html = html[:css_start] + html[css_end:]

# 2. Replace static background HTML with continuous Canvas
bg_html_start = html.find('<!-- Background Elements (Always present) -->')
bg_html_end = html.find('<!-- LANDING PAGE -->')
if bg_html_start != -1 and bg_html_end != -1:
    canvas_html = '''  <!-- CONTINUOUS CANVAS BACKGROUND -->
  <canvas id="node-canvas" class="fixed inset-0 z-0 opacity-75 pointer-events-none"></canvas>

'''
    html = html[:bg_html_start] + canvas_html + html[bg_html_end:]

# 3. Make landing page completely transparent so canvas shows
html = html.replace('bg-black/80 backdrop-blur-sm', 'bg-transparent')
html = html.replace('bg-[#030712]', 'bg-gray-950')
html = html.replace('bg-black/50', 'bg-gray-900/30') # make header transparent

# Make sure main wrapper is properly structured
html = html.replace('id="landing-view" class="fixed inset-0 z-50', 'id="landing-view" class="fixed inset-0 z-50')

# 4. Inject High-Performance Canvas Renderer
script_start = html.find('<script>') + len('<script>')
canvas_js = '''
    // --- Continuous Background Canvas Animation ---
    const canvas = document.getElementById('node-canvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      let w, h, nodes = [];
      function resize() { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; }
      function initNodes() {
          resize();
          nodes = [];
          
          // Generate 120 dynamic connection nodes
          for(let i=0; i<120; i++) {
              nodes.push({
                  x: Math.random() * w, 
                  y: Math.random() * h,
                  vx: (Math.random() - 0.5) * 1.2, 
                  vy: (Math.random() - 0.5) * 1.2,
                  radius: Math.random() * 2 + 1
              });
          }
      }
      
      // Main Animation Loop runs indefinitely across both views
      function drawNodes() {
          ctx.clearRect(0, 0, w, h);
          
          // Update and draw points
          nodes.forEach(node => {
              node.x += node.vx; node.y += node.vy;
              
              // Bounce off walls organically
              if(node.x < 0 || node.x > w) node.vx *= -1;
              if(node.y < 0 || node.y > h) node.vy *= -1;
              
              ctx.beginPath(); 
              ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
              ctx.fillStyle = 'rgba(34, 211, 238, 0.5)'; 
              ctx.fill();
          });
          
          // Draw geometric connection lines natively
          ctx.lineWidth = 0.6;
          for(let i=0; i<nodes.length; i++) {
              for(let j=i+1; j<nodes.length; j++) {
                  let dx = nodes[i].x - nodes[j].x;
                  let dy = nodes[i].y - nodes[j].y;
                  let dist = Math.sqrt(dx*dx + dy*dy);
                  
                  if(dist < 150) {
                      ctx.beginPath(); 
                      ctx.moveTo(nodes[i].x, nodes[i].y); 
                      ctx.lineTo(nodes[j].x, nodes[j].y);
                      ctx.strokeStyle = `rgba(99, 102, 241, ${0.5 - dist/300})`; 
                      ctx.stroke();
                  }
              }
          }
          requestAnimationFrame(drawNodes);
      }
      
      window.addEventListener('resize', initNodes);
      initNodes();
      drawNodes(); // Unleash the render loop
    }
'''
html = html[:script_start] + canvas_js + html[script_start:]

# 5. Hide the Landing View using visibility instead of completely `display: none` 
# Actually `hidden` is fine, since canvas is outside, making landing hidden reveals dashboard under it.
# To make the transition absolutely spotless: 
html = html.replace("landing.classList.add('hidden');", "landing.style.pointerEvents = 'none';")

with codecs.open('c:/Users/upadh/haack/index.html', 'w', 'utf-8') as f:
    f.write(html)
