import os
with open('c:/Users/upadh/haack/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Background Animation injected into body
bg_anim = '''<body class="min-h-screen relative selection:bg-indigo-500/30 overflow-x-hidden bg-[#030712]">
  <!-- Animated Background Elements -->
  <div class="fixed inset-0 z-[-1] pointer-events-none overflow-hidden">
    <div class="absolute top-[-20%] left-[-10%] w-[70vw] h-[70vw] bg-indigo-600/10 blur-[150px] rounded-full animate-[spin_20s_linear_infinite]"></div>
    <div class="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-cyan-600/10 blur-[150px] rounded-full animate-[spin_25s_linear_infinite_reverse]"></div>
    <div class="absolute inset-0" style="background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px); background-size: 60px 60px; transform: perspective(500px) rotateX(60deg) scale(2) translateY(-100px); animation: gridMove 20s linear infinite;"></div>
  </div>
  <style>@keyframes gridMove { 0% { transform: perspective(500px) rotateX(60deg) scale(2) translateY(0); } 100% { transform: perspective(500px) rotateX(60deg) scale(2) translateY(60px); } }</style>
'''
text = text.replace('<body class="min-h-screen relative selection:bg-indigo-500/30 overflow-x-hidden">', bg_anim)

# 2. Disable Dashboard auto-scan 
old_launch = '''setTimeout(() => {
            const btn = document.getElementById('btn-scan');
            if(btn) btn.classList.add('hidden');
            if(typeof startScan === 'function') startScan();
          }, 300);'''
text = text.replace(old_launch, '// auto scan disabled per user request')

# 3. Add Empty State & Fix DOM animation overwrite glitch 
# If html equals what was already there, don't innerHTML replace
old_render_end = '''const isFirstRender = container.innerHTML.trim() === '';
      container.innerHTML = html;
      if (isFirstRender) {
        gsap.from('.glass-card', {
          y: 40,
          opacity: 0,
          duration: 0.6,
          stagger: 0.05,
          ease: 'power2.out'
        });
      }'''
new_render_end = '''const isFirstRender = container.innerHTML.trim() === '' || container.innerHTML.includes('Systems Dormant');
      
      // Update DOM only if changes occurred, preventing CSS anim overrides
      if (container.innerHTML !== html) {
          container.innerHTML = html;
      }
      
      if (isFirstRender && globalServers.length > 0) {
        gsap.fromTo('.glass-card', 
          { y: 50, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.8, stagger: 0.05, ease: 'power3.out' }
        );
      }'''
text = text.replace(old_render_end, new_render_end)

with open('c:/Users/upadh/haack/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
