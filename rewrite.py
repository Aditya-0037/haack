import os

with open('c:/Users/upadh/haack/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove ThreeJS Script tag
html = html.replace('  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n', '')

# 2. Replace the Hero Canvas HTML entirely with the V4 Landing HTML
v4_landing = """  <!-- ANIMATED LANDING PAGE -->
  <div id="landing-view" class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[#030712] overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-[10%] left-[10%] w-[60vw] h-[60vw] rounded-full bg-indigo-600/10 blur-[130px] animate-[pulse_8s_ease-in-out_infinite]"></div>
      <div class="absolute bottom-[10%] right-[10%] w-[50vw] h-[50vw] rounded-full bg-cyan-600/10 blur-[130px] animate-[pulse_10s_ease-in-out_infinite_reverse]"></div>
    </div>
    <div class="relative z-10 flex flex-col items-center px-6">
      <div class="w-24 h-24 mb-10 rounded-3xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center shadow-[0_0_50px_rgba(99,102,241,0.5)] animate-bounce" style="animation-duration: 3s;">
        <svg class="w-12 h-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
      </div>
      <h1 class="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-500 tracking-tighter mb-6 text-center leading-[1.1]">
        Cloud Healer <br/><span class="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">Nexus</span>
      </h1>
      <p class="text-gray-400 text-lg md:text-xl max-w-2xl text-center mb-16 font-light tracking-wide leading-relaxed">
        Next-generation autonomous dashboard interface. Engage the core cluster to orchestrate live secure nodes.
      </p>
      <button onclick="launchDashboard()" class="relative group px-1.5 py-1.5 rounded-full overflow-hidden transition-all duration-500 hover:scale-[1.03] active:scale-95 shadow-[0_0_30px_rgba(99,102,241,0.2)] hover:shadow-[0_0_60px_rgba(6,182,212,0.4)]">
        <div class="absolute inset-[-100%] bg-[conic-gradient(from_90deg,transparent_0%,transparent_50%,#4f46e5_50%,#22d3ee_100%)] animate-[spin_3s_linear_infinite] group-hover:animate-[spin_1s_linear_infinite]"></div>
        <div class="absolute inset-[3px] bg-[#030712] rounded-full group-hover:bg-gray-950 transition-colors"></div>
        <div class="relative z-10 flex items-center gap-4 px-12 py-5 font-bold text-white text-lg tracking-widest uppercase transition-colors duration-300">
          Engage System
          <svg class="w-6 h-6 group-hover:translate-x-2 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </div>
      </button>
    </div>
  </div>"""

parts = html.split('<!-- THREE.JS HERO INTERACTION -->')
if len(parts) == 2:
    subparts = parts[1].split('<div id="dashboard-view"', 1)
    if len(subparts) == 2:
        html = parts[0] + v4_landing + '\n\n  <div id="dashboard-view"' + subparts[1]
        print("Successfully replaced HTML landing view.")

# 3. Replace the ThreeJS script block
js_replacement = """    // --- Landing Transition & GSAP Stagger ---
    function launchDashboard() {
      const landing = document.getElementById('landing-view');
      const dash = document.getElementById('dashboard-view');
      gsap.to(landing, {
        opacity: 0, scale: 1.05, duration: 1.0, ease: 'power3.inOut',
        onComplete: () => {
          landing.classList.add('hidden');
          dash.classList.remove('hidden', 'opacity-0');
          gsap.from('.glass-header', { y: -30, opacity: 0, duration: 1, ease: 'power3.out' });
          setTimeout(() => {
            const btn = document.getElementById('btn-scan');
            if(btn) btn.classList.add('hidden');
            if(typeof startScan === 'function') startScan();
          }, 300);
        }
      });
    }"""

parts_js = html.split('// --- Three.js Hero Interaction ---')
if len(parts_js) == 2:
    subparts_js = parts_js[1].split('async function startScan()', 1)
    if len(subparts_js) == 2:
        html = parts_js[0] + js_replacement + '\n\n    async function startScan()' + subparts_js[1]
        print("Successfully replaced JS logic.")

# 4. Inject GSAP stagger into renderGrid
# Note: we are looking for the end of the renderGrid function.
renderGridOld = 'container.innerHTML = html;\n    }'
renderGridNew = '''const isFirstRender = container.innerHTML.trim() === '';
      container.innerHTML = html;
      if (isFirstRender) {
        gsap.from('.glass-card', {
          y: 40,
          opacity: 0,
          duration: 0.6,
          stagger: 0.05,
          ease: 'power2.out'
        });
      }
    }'''
if renderGridOld in html:
    html = html.replace(renderGridOld, renderGridNew)
    print("Successfully replaced renderGrid.")
else:
    print("renderGrid target not found! Using fallback matching.")
    html = html.replace('      container.innerHTML = html;\r\n    }', renderGridNew)

# Fix dashboard transition class if present
html = html.replace('duration-[1500ms]', 'duration-500')

with open('c:/Users/upadh/haack/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html successfully updated!")
