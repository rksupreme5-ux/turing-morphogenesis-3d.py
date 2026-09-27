#!/usr/bin/env python3
"""
===============================================================================
 TURING-OS // 3D MORPHOGENESIS & REACTION-DIFFUSION PDE ENGINE (WSL + VS CODE)
===============================================================================
 Run in VS Code WSL Ubuntu Terminal:
     python3 turing_morphogenesis.py
===============================================================================
"""

import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import time
from urllib.parse import urlparse

# ANSI Terminal Colors for Live VS Code Ubuntu Terminal Telemetry
ORANGE = "\033[38;5;208m"
GOLD = "\033[93m"
CRIMSON = "\033[91m"
WHITE = "\033[97m"
GREEN = "\033[92m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

HTML_PAYLOAD = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TURING-OS // 3D Morphogenesis & Reaction-Diffusion Engine</title>
  <style>
    :root {
      --bg-charcoal: #090706;
      --panel-bg: rgba(18, 14, 12, 0.86);
      --border-gold: rgba(255, 168, 52, 0.32);
      --solar: #ff5e1a;
      --gold: #ffc44d;
      --ivory: #f7f3eb;
      --crimson: #ff2a55;
      --muted: #9c8d7e;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      background: radial-gradient(circle at 54% 48%, #1f140e 0%, #080605 80%);
      color: var(--ivory);
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }

    #canvas-container {
      position: fixed;
      inset: 0;
      z-index: 1;
    }

    /* Architectural Blueprint Crosshair Backdrop */
    .blueprint-overlay {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 2;
      background-image:
        radial-gradient(rgba(255, 196, 77, 0.14) 1px, transparent 1px),
        linear-gradient(to right, rgba(255, 140, 50, 0.025) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 140, 50, 0.025) 1px, transparent 1px);
      background-size: 36px 36px, 144px 144px, 144px 144px;
      mask-image: radial-gradient(circle at center, rgba(0,0,0,0.9) 25%, transparent 85%);
    }

    /* Chamfered Sci-Fi Architectural Card Style */
    .chamfer-box {
      background: var(--panel-bg);
      border: 1px solid var(--border-gold);
      backdrop-filter: blur(16px);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(255, 220, 160, 0.12);
      clip-path: polygon(
        0 10px, 10px 0,
        calc(100% - 10px) 0, 100% 10px,
        100% calc(100% - 10px), calc(100% - 10px) 100%,
        10px 100%, 0 calc(100% - 10px)
      );
    }

    /* ==================== TOP ARCHITECTURAL TELEMETRY RIBBON ==================== */
    .top-ribbon {
      position: fixed;
      top: 14px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 18px;
      padding: 10px 24px;
      white-space: nowrap;
      transition: opacity 0.3s ease;
    }

    .sys-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      padding-right: 16px;
      border-right: 1px solid rgba(255, 196, 77, 0.22);
    }

    .sys-orb {
      width: 12px;
      height: 12px;
      background: var(--solar);
      transform: rotate(45deg);
      box-shadow: 0 0 12px var(--solar);
      animation: rotateOrb 6s linear infinite;
    }

    @keyframes rotateOrb {
      0% { transform: rotate(45deg) scale(1); }
      50% { transform: rotate(225deg) scale(1.2); }
      100% { transform: rotate(405deg) scale(1); }
    }

    .sys-title {
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 2.2px;
      color: var(--gold);
      text-transform: uppercase;
    }

    .sys-sub {
      font-size: 9.5px;
      color: var(--muted);
      letter-spacing: 1.4px;
    }

    .pde-formula {
      font-family: 'Cambria Math', 'Times New Roman', serif;
      font-size: 15.5px;
      color: var(--ivory);
      padding-right: 16px;
      border-right: 1px solid rgba(255, 196, 77, 0.22);
    }

    .pde-formula .so { color: var(--solar); font-weight: 700; }
    .pde-formula .go { color: var(--gold); font-weight: 700; }

    .top-metrics {
      display: flex;
      gap: 16px;
    }

    .t-metric {
      display: flex;
      flex-direction: column;
    }

    .t-label {
      font-size: 9px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--muted);
    }

    .t-val {
      font-family: 'Consolas', monospace;
      font-size: 13.5px;
      font-weight: 700;
      color: var(--gold);
    }

    /* ==================== LEFT VERTICAL COMMAND SPINE ==================== */
    .left-spine {
      position: fixed;
      top: 84px;
      left: 16px;
      width: 285px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: opacity 0.3s ease;
    }

    .panel-pad {
      padding: 14px 16px;
    }

    .hdr-line {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 2.2px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 196, 77, 0.16);
      padding-bottom: 5px;
    }

    /* 3D Topology Selector Grid */
    .topo-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
    }

    .arch-btn {
      background: rgba(255, 168, 52, 0.07);
      border: 1px solid rgba(255, 168, 52, 0.25);
      color: var(--ivory);
      padding: 8px 10px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.16s ease;
      text-align: left;
      clip-path: polygon(0 5px, 5px 0, 100% 0, 100% calc(100% - 5px), calc(100% - 5px) 100%, 0 100%);
    }

    .arch-btn:hover {
      background: rgba(255, 94, 26, 0.22);
      border-color: var(--solar);
      transform: translateX(2px);
    }

    .arch-btn.active {
      background: linear-gradient(135deg, rgba(255, 94, 26, 0.42), rgba(255, 196, 77, 0.28));
      border-color: var(--gold);
      color: #fff;
      box-shadow: 0 0 15px rgba(255, 94, 26, 0.35);
    }

    /* Biological Regime List */
    .regime-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .regime-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 196, 77, 0.18);
      padding: 8px 11px;
      cursor: pointer;
      transition: all 0.16s ease;
      color: var(--ivory);
      font-size: 11px;
      font-weight: 700;
    }

    .regime-item:hover {
      background: rgba(255, 196, 77, 0.14);
      border-color: var(--gold);
    }

    .regime-item.active {
      background: linear-gradient(90deg, rgba(255, 94, 26, 0.38), rgba(255, 196, 77, 0.12));
      border-left: 4px solid var(--solar);
      border-color: var(--gold);
    }

    .fk-tag {
      font-family: 'Consolas', monospace;
      font-size: 9.5px;
      color: var(--gold);
      opacity: 0.9;
    }

    /* Material Shader Switcher */
    .shader-row {
      display: flex;
      gap: 6px;
    }

    .shader-row .arch-btn {
      flex: 1;
      text-align: center;
      padding: 7px 4px;
      font-size: 10.5px;
    }

    /* ==================== RIGHT CHEMICAL PAINTER & PHASE LAB ==================== */
    .right-lab {
      position: fixed;
      top: 84px;
      right: 16px;
      width: 310px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: opacity 0.3s ease;
    }

    .painter-frame {
      position: relative;
      border: 1px solid rgba(255, 196, 77, 0.35);
      background: #050403;
      overflow: hidden;
    }

    #chemCanvas {
      display: block;
      width: 100%;
      height: 210px;
      cursor: crosshair;
    }

    .painter-overlay-tag {
      position: absolute;
      top: 6px;
      left: 8px;
      background: rgba(9, 7, 6, 0.82);
      border: 1px solid rgba(255, 196, 77, 0.3);
      padding: 2px 7px;
      font-family: 'Consolas', monospace;
      font-size: 9.5px;
      color: var(--gold);
      pointer-events: none;
    }

    .painter-hint {
      font-size: 10px;
      color: var(--muted);
      text-align: center;
      margin-top: 6px;
    }

    /* Sliders */
    .ctrl-row {
      margin-bottom: 9px;
    }
    .ctrl-row:last-child { margin-bottom: 0; }

    .ctrl-head {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      margin-bottom: 4px;
      color: #ede4d7;
    }

    .ctrl-val {
      font-family: 'Consolas', monospace;
      color: var(--gold);
      font-weight: 700;
    }

    input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 5px;
      background: linear-gradient(90deg, rgba(255, 94, 26, 0.4), rgba(255, 196, 77, 0.4));
      outline: none;
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 13px;
      height: 13px;
      background: var(--gold);
      border: 2px solid #090706;
      transform: rotate(45deg);
      box-shadow: 0 0 10px var(--solar);
      cursor: pointer;
    }

    /* ==================== BOTTOM TURNTABLE CONSOLE ==================== */
    .bottom-console {
      position: fixed;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 9px 18px;
      transition: opacity 0.3s ease;
    }

    .console-btn {
      background: rgba(255, 196, 77, 0.08);
      border: 1px solid rgba(255, 196, 77, 0.28);
      color: var(--ivory);
      padding: 7px 13px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      clip-path: polygon(0 4px, 4px 0, 100% 0, 100% calc(100% - 4px), calc(100% - 4px) 100%, 0 100%);
      white-space: nowrap;
    }

    .console-btn:hover {
      background: rgba(255, 94, 26, 0.28);
      border-color: var(--solar);
      transform: translateY(-2px);
    }

    .console-btn.active {
      background: rgba(255, 94, 26, 0.35);
      border-color: var(--gold);
      color: var(--gold);
      box-shadow: 0 0 12px rgba(255, 94, 26, 0.35);
    }

    .console-btn.action-seed {
      background: linear-gradient(135deg, rgba(255, 94, 26, 0.35), rgba(255, 42, 85, 0.35));
      border-color: var(--solar);
      color: #ffd8be;
    }

    .sep {
      width: 1px;
      height: 22px;
      background: rgba(255, 196, 77, 0.22);
      margin: 0 4px;
    }

    .ui-hidden .left-spine,
    .ui-hidden .right-lab,
    .ui-hidden .bottom-console {
      opacity: 0;
      pointer-events: none;
    }

    @media (max-width: 1100px) {
      .left-spine { display: none; }
      .pde-formula { display: none; }
    }
  </style>

  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }
  </script>
</head>
<body>

  <div id="canvas-container"></div>
  <div class="blueprint-overlay"></div>

  <!-- ==================== TOP ARCHITECTURAL TELEMETRY RIBBON ==================== -->
  <div class="top-ribbon chamfer-box">
    <div class="sys-badge">
      <div class="sys-orb"></div>
      <div>
        <div class="sys-title">TURING-OS // MORPHOGENESIS 3D</div>
        <div class="sys-sub">COUPLED REACTION–DIFFUSION PDE MANIFOLD</div>
      </div>
    </div>

    <div class="pde-formula">
      ∂<sub>t</sub><span class="go">U</span> = D<sub>u</sub>∇²<span class="go">U</span> − <span class="go">U</span><span class="so">V²</span> + F(1−<span class="go">U</span>) , &nbsp;
      ∂<sub>t</sub><span class="so">V</span> = D<sub>v</sub>∇²<span class="so">V</span> + <span class="go">U</span><span class="so">V²</span> − (F+k)<span class="so">V</span>
    </div>

    <div class="top-metrics">
      <div class="t-metric">
        <span class="t-label">Morphogen ⟨V⟩</span>
        <span class="t-val" id="valMeanV">0.284 mol/L</span>
      </div>
      <div class="t-metric">
        <span class="t-label">Pattern Entropy H</span>
        <span class="t-val" id="valEntropy" style="color:#ff7b42;">3.82 bits</span>
      </div>
      <div class="t-metric">
        <span class="t-label">Turing λ_T</span>
        <span class="t-val" id="valLambda">14.2 μm</span>
      </div>
      <div class="t-metric">
        <span class="t-label">PDE Steps</span>
        <span class="t-val" id="valSteps" style="color:#fff;">0</span>
      </div>
    </div>
  </div>

  <!-- ==================== LEFT VERTICAL COMMAND SPINE ==================== -->
  <div class="left-spine">
    <!-- 3D Manifold Topology Switcher -->
    <div class="chamfer-box panel-pad">
      <div class="hdr-line">
        <span>1. 3D Manifold Topology</span>
        <span style="font-size:9px;color:var(--solar);">SMOOTH MORPH</span>
      </div>
      <div class="topo-grid">
        <button class="arch-btn active" data-topo="0">🌐 Bio-Sphere</button>
        <button class="arch-btn" data-topo="1">🍩 Torus Reactor</button>
        <button class="arch-btn" data-topo="2">🪸 Coral Gyroid</button>
        <button class="arch-btn" data-topo="3">🐚 Nautilus Spire</button>
      </div>
    </div>

    <!-- 5 Gray-Scott Biological Regimes -->
    <div class="chamfer-box panel-pad">
      <div class="hdr-line">
        <span>2. Turing Reaction Regime</span>
        <span style="font-size:9px;color:var(--muted);">(F, k) SPACE</span>
      </div>
      <div class="regime-list">
        <div class="regime-item active" data-regime="coral">
          <span>🧠 Brain Cortex Labyrinth</span>
          <span class="fk-tag">F=0.029 k=0.057</span>
        </div>
        <div class="regime-item" data-regime="mitosis">
          <span>🦠 Cellular Mitosis Division</span>
          <span class="fk-tag">F=0.037 k=0.065</span>
        </div>
        <div class="regime-item" data-regime="spirals">
          <span>🌀 Belousov Spiral Waves</span>
          <span class="fk-tag">F=0.018 k=0.051</span>
        </div>
        <div class="regime-item" data-regime="spots">
          <span>🐆 Soliton Leopard Spots</span>
          <span class="fk-tag">F=0.035 k=0.060</span>
        </div>
        <div class="regime-item" data-regime="worms">
          <span>🪱 Vermicular Coral Ridges</span>
          <span class="fk-tag">F=0.054 k=0.063</span>
        </div>
      </div>
    </div>

    <!-- Surface Material Shader -->
    <div class="chamfer-box panel-pad">
      <div class="hdr-line">
        <span>3. Surface Material Shader</span>
      </div>
      <div class="shader-row">
        <button class="arch-btn active" data-shader="0">🌋 Molten Gold</button>
        <button class="arch-btn" data-shader="1">🏺 Kintsugi</button>
        <button class="arch-btn" data-shader="2">💿 Chrome</button>
      </div>
    </div>
  </div>

  <!-- ==================== RIGHT CHEMICAL PAINTER & PDE CONTROLS ==================== -->
  <div class="right-lab">
    <!-- Live 2D Chemical Field Painter (Maps Directly onto 3D Surface) -->
    <div class="chamfer-box panel-pad">
      <div class="hdr-line">
        <span>Live 2D→3D Catalyst Brush</span>
        <button class="arch-btn" id="btnSeedBurst" style="padding:2px 8px;font-size:9.5px;">+ Inject Drop</button>
      </div>
      <div class="painter-frame">
        <div class="painter-overlay-tag" id="overlayFK">GRAY-SCOTT FIELD V(u,v)</div>
        <canvas id="chemCanvas" width="128" height="128"></canvas>
      </div>
      <div class="painter-hint">Draw inside box to paint chemical V onto the 3D sculpture</div>
    </div>

    <!-- PDE & 3D Extrusion Sliders -->
    <div class="chamfer-box panel-pad">
      <div class="hdr-line">
        <span>PDE &amp; 3D Relief Parameters</span>
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>3D Ridge Extrusion Amplitude</span>
          <span class="ctrl-val" id="lblExtrude">0.72</span>
        </div>
        <input type="range" id="slExtrude" min="0.05" max="1.60" step="0.02" value="0.72" />
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>Feed Rate (F — Activator Supply)</span>
          <span class="ctrl-val" id="lblFeed">0.0290</span>
        </div>
        <input type="range" id="slFeed" min="0.010" max="0.070" step="0.0005" value="0.0290" />
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>Kill Rate (k — Catalyst Decay)</span>
          <span class="ctrl-val" id="lblKill">0.0570</span>
        </div>
        <input type="range" id="slKill" min="0.040" max="0.070" step="0.0005" value="0.0570" />
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>Turntable Spin Speed (Ω)</span>
          <span class="ctrl-val" id="lblSpin">0.65 rad/s</span>
        </div>
        <input type="range" id="slSpin" min="0" max="3.5" step="0.05" value="0.65" />
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>PDE Time-Warp (Substeps/Frame)</span>
          <span class="ctrl-val" id="lblSubsteps">10x</span>
        </div>
        <input type="range" id="slSubsteps" min="1" max="24" step="1" value="10" />
      </div>

      <div class="ctrl-row">
        <div class="ctrl-head">
          <span>Solar Bloom Radiance</span>
          <span class="ctrl-val" id="lblBloom">0.85</span>
        </div>
        <input type="range" id="slBloom" min="0.1" max="2.2" step="0.05" value="0.85" />
      </div>
    </div>
  </div>

  <!-- ==================== BOTTOM TURNTABLE CONSOLE ==================== -->
  <div class="bottom-console chamfer-box">
    <button class="console-btn active" id="btnToggleSpin">⏸ Spin</button>
    <button class="console-btn" id="btnReverseSpin">⇄ Reverse</button>
    <button class="console-btn" id="btnTumble">🪐 3-Axis Tumble</button>

    <div class="sep"></div>

    <button class="console-btn action-seed" id="btnMitosisWave">⚡ Trigger Catalyst Wave</button>
    <button class="console-btn" id="btnClearField">🧹 Reset Substrate</button>

    <div class="sep"></div>

    <button class="console-btn" id="camFront">Front</button>
    <button class="console-btn" id="camTop">Zenith</button>
    <button class="console-btn" id="camClose">Macro</button>
    <button class="console-btn" id="btnCinema" title="Shortcut: H">👁️ Cinema</button>
  </div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

    // =========================================================================
    // 1. THREE.JS SCENE, CAMERA, RENDERER & POST-PROCESSING
    // =========================================================================
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 150);
    camera.position.set(0, 2.0, 9.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 25;
    controls.minDistance = 2.5;

    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));

    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      0.85, 0.45, 0.22
    );
    composer.addPass(bloomPass);

    // Architectural Turntable Base Ring
    const baseGroup = new THREE.Group();
    baseGroup.position.y = -3.35;
    const ring1 = new THREE.Mesh(
      new THREE.RingGeometry(3.2, 3.25, 96).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: 0xffa834, side: THREE.DoubleSide, transparent: true, opacity: 0.32 })
    );
    const ring2 = new THREE.Mesh(
      new THREE.RingGeometry(4.4, 4.42, 96).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: 0xff5e1a, side: THREE.DoubleSide, transparent: true, opacity: 0.20 })
    );
    baseGroup.add(ring1, ring2);
    scene.add(baseGroup);

    // =========================================================================
    // 2. COUPLED 2D GRAY-SCOTT REACTION-DIFFUSION PDE SOLVER (128x128 PERIODIC)
    // =========================================================================
    const N = 128;
    const SIZE = N * N;
    let U = new Float32Array(SIZE);
    let V = new Float32Array(SIZE);
    let nextU = new Float32Array(SIZE);
    let nextV = new Float32Array(SIZE);

    const state = {
      regime: 'coral',
      topology: 0,       // 0: Sphere, 1: Torus, 2: Coral Gyroid, 3: Nautilus Spire
      shaderMode: 0,     // 0: Molten Gold, 1: Kintsugi Porcelain, 2: Cyber-Chrome
      spinning: true,
      spinDir: 1,
      tumble: false,
      spinSpeed: 0.65,
      extrude: 0.72,
      F: 0.0290,
      k: 0.0570,
      Du: 1.0,
      Dv: 0.5,
      substeps: 10,
      totalSteps: 0,
      meanV: 0.28,
      entropy: 3.82
    };

    // Seed the Gray-Scott substrate with symmetric biological nucleation sites
    function seedReactionField(clearFirst = true) {
      if (clearFirst) {
        U.fill(1.0);
        V.fill(0.0);
        state.totalSteps = 0;
      }

      const spots = 18;
      for (let s = 0; s < spots; s++) {
        const cx = Math.floor(Math.random() * N);
        const cy = Math.floor(Math.random() * N);
        const rad = 3 + Math.floor(Math.random() * 4);
        for (let dy = -rad; dy <= rad; dy++) {
          for (let dx = -rad; dx <= rad; dx++) {
            if (dx * dx + dy * dy <= rad * rad) {
              const x = (cx + dx + N) % N;
              const y = (cy + dy + N) % N;
              const idx = y * N + x;
              U[idx] = 0.50 + (Math.random() - 0.5) * 0.08;
              V[idx] = 0.25 + (Math.random() - 0.5) * 0.08;
            }
          }
        }
      }
    }

    seedReactionField(true);

    // Run 9-Point Isotropic Laplacian Gray-Scott Integration Step
    function stepGrayScottPDE() {
      const F = state.F;
      const k = state.k;
      const Du = state.Du;
      const Dv = state.Dv;
      const dt = 0.92;

      for (let y = 0; y < N; y++) {
        const ym = ((y - 1 + N) % N) * N;
        const yc = y * N;
        const yp = ((y + 1) % N) * N;

        for (let x = 0; x < N; x++) {
          const xm = (x - 1 + N) % N;
          const xp = (x + 1) % N;
          const idx = yc + x;

          const u = U[idx];
          const v = V[idx];

          // 9-point isotropic discrete Laplacian
          const lapU =
            0.20 * (U[yc + xm] + U[yc + xp] + U[ym + x] + U[yp + x]) +
            0.05 * (U[ym + xm] + U[ym + xp] + U[yp + xm] + U[yp + xp]) -
            u;

          const lapV =
            0.20 * (V[yc + xm] + V[yc + xp] + V[ym + x] + V[yp + x]) +
            0.05 * (V[ym + xm] + V[ym + xp] + V[yp + xm] + V[yp + xp]) -
            v;

          const uvv = u * v * v;
          let nu = u + dt * (Du * lapU - uvv + F * (1.0 - u));
          let nv = v + dt * (Dv * lapV + uvv - (F + k) * v);

          nextU[idx] = nu < 0.0 ? 0.0 : (nu > 1.0 ? 1.0 : nu);
          nextV[idx] = nv < 0.0 ? 0.0 : (nv > 1.0 ? 1.0 : nv);
        }
      }

      // Swap buffers
      const tmpU = U; U = nextU; nextU = tmpU;
      const tmpV = V; V = nextV; nextV = tmpV;
      state.totalSteps++;
    }

    // Warm up 180 steps on startup so an intricate pattern is immediately visible
    for (let w = 0; w < 180; w++) stepGrayScottPDE();

    // =========================================================================
    // 3. GPU DATA-TEXTURE & 2D INTERACTIVE CATALYST PAINTER
    // =========================================================================
    const texData = new Uint8Array(SIZE * 4);
    const chemTexture = new THREE.DataTexture(texData, N, N, THREE.RGBAFormat, THREE.UnsignedByteType);
    chemTexture.wrapS = THREE.RepeatWrapping;
    chemTexture.wrapT = THREE.RepeatWrapping;
    chemTexture.minFilter = THREE.LinearFilter;
    chemTexture.magFilter = THREE.LinearFilter;

    const chemCanvas = document.getElementById('chemCanvas');
    const chemCtx = chemCanvas.getContext('2d');
    const canvasImg = chemCtx.createImageData(N, N);

    function syncTextureAnd2DCanvas() {
      const cData = canvasImg.data;
      let sumV = 0;

      for (let y = 0; y < N; y++) {
        const ym = ((y - 1 + N) % N) * N;
        const yc = y * N;
        const yp = ((y + 1) % N) * N;

        for (let x = 0; x < N; x++) {
          const xm = (x - 1 + N) % N;
          const xp = (x + 1) % N;
          const i = yc + x;
          const i4 = i * 4;

          const u = U[i];
          const v = V[i];
          sumV += v;

          // Spatial gradients dV/dx, dV/dy packed into B and A channels for crisp 3D bump lighting
          const gx = (V[yc + xp] - V[yc + xm]) * 2.2;
          const gy = (V[yp + x] - V[ym + x]) * 2.2;

          const vNorm = Math.min(1.0, v * 2.3);
          texData[i4]     = Math.floor(u * 255);
          texData[i4 + 1] = Math.floor(vNorm * 255);
          texData[i4 + 2] = Math.floor(Math.max(0, Math.min(1, 0.5 + gx)) * 255);
          texData[i4 + 3] = Math.floor(Math.max(0, Math.min(1, 0.5 + gy)) * 255);

          // 2D Painter Colormap (Matches selected shader theme)
          if (state.shaderMode === 1) {
            // Kintsugi Porcelain & Gold
            cData[i4]     = Math.floor(242 - vNorm * 30);
            cData[i4 + 1] = Math.floor(236 - vNorm * 65);
            cData[i4 + 2] = Math.floor(225 - vNorm * 175);
            cData[i4 + 3] = 255;
          } else {
            // Molten Obsidian & Solar Gold
            cData[i4]     = Math.floor(14 + Math.pow(vNorm, 0.75) * 241);
            cData[i4 + 1] = Math.floor(10 + Math.pow(vNorm, 1.35) * 195);
            cData[i4 + 2] = Math.floor(9  + Math.pow(vNorm, 2.60) * 110);
            cData[i4 + 3] = 255;
          }
        }
      }

      chemTexture.needsUpdate = true;
      chemCtx.putImageData(canvasImg, 0, 0);

      state.meanV = sumV / SIZE;
      const p = Math.max(0.01, Math.min(0.99, state.meanV * 2.1));
      state.entropy = -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p)) * 4.2;
      const lambda = (11.5 + (state.Du / (state.F + 0.01)) * 0.12).toFixed(1);

      document.getElementById('valMeanV').textContent = `${state.meanV.toFixed(3)} mol/L`;
      document.getElementById('valEntropy').textContent = `${state.entropy.toFixed(2)} bits`;
      document.getElementById('valLambda').textContent = `${lambda} μm`;
      document.getElementById('valSteps').textContent = state.totalSteps.toLocaleString();
    }

    // Interactive Mouse Painting on the 2D Chemical Canvas
    let isPainting = false;
    function paintAtEvent(e) {
      const rect = chemCanvas.getBoundingClientRect();
      const cx = Math.floor(((e.clientX - rect.left) / rect.width) * N);
      const cy = Math.floor(((e.clientY - rect.top) / rect.height) * N);
      const rad = 5;
      for (let dy = -rad; dy <= rad; dy++) {
        for (let dx = -rad; dx <= rad; dx++) {
          if (dx * dx + dy * dy <= rad * rad) {
            const x = (cx + dx + N) % N;
            const y = (cy + dy + N) % N;
            const idx = y * N + x;
            U[idx] = 0.45;
            V[idx] = 0.35;
          }
        }
      }
    }
    chemCanvas.addEventListener('pointerdown', (e) => { isPainting = true; paintAtEvent(e); });
    window.addEventListener('pointerup', () => { isPainting = false; });
    chemCanvas.addEventListener('pointermove', (e) => { if (isPainting) paintAtEvent(e); });

    // =========================================================================
    // 4. 3D PARAMETRIC MORPHOGENESIS MANIFOLD & CUSTOM GLSL SHADER
    // =========================================================================
    const morphUniforms = {
      uChemTex: { value: chemTexture },
      uTime: { value: 0 },
      uExtrude: { value: state.extrude },
      uShaderMode: { value: 0 },
      uTopoWeights: { value: new THREE.Vector4(1, 0, 0, 0) } // Smoothly blends 4 topologies!
    };

    const vertexShader = `
      uniform sampler2D uChemTex;
      uniform float uTime;
      uniform float uExtrude;
      uniform vec4 uTopoWeights;

      varying vec2 vUv;
      varying vec3 vWorldPos;
      varying vec3 vBaseNormal;
      varying float vChemV;

      const float PI = 3.14159265359;

      // Evaluate position and outward normal for each of the 4 3D Topologies
      void evalTopologies(vec2 uv, out vec3 pos, out vec3 norm) {
        float u = uv.x * 2.0 * PI;
        float v = uv.y * 2.0 * PI;
        float theta = uv.y * PI;

        // 0. Bio-Sphere (Seamless Periodic UV mapping)
        vec3 p0 = vec3(
          2.35 * sin(theta) * cos(u),
          2.35 * cos(theta),
          2.35 * sin(theta) * sin(u)
        );
        vec3 n0 = normalize(p0);

        // 1. Toroidal Bio-Reactor (R = 2.15, r = 0.95)
        float R1 = 2.15;
        float r1 = 0.95;
        vec3 p1 = vec3(
          (R1 + r1 * cos(v)) * cos(u),
          r1 * sin(v),
          (R1 + r1 * cos(v)) * sin(u)
        );
        vec3 n1 = normalize(vec3(cos(v) * cos(u), sin(v), cos(v) * sin(u)));

        // 2. Hyperbolic Coral Gyroid-Inspired Multi-Lobe Reef
        float lobe = 2.05 + 0.55 * (sin(3.0 * u) * sin(2.0 * v) + cos(2.0 * u) * cos(3.0 * v));
        vec3 p2 = vec3(
          lobe * sin(theta) * cos(u),
          lobe * cos(theta) + 0.35 * sin(2.0 * u),
          lobe * sin(theta) * sin(u)
        );
        vec3 n2 = normalize(p2);

        // 3. Nautilus Helical Spire
        float spireT = uv.y * 2.0 * PI;
        float spireR = 0.65 + 1.45 * sin(uv.y * PI);
        vec3 p3 = vec3(
          (spireR + 0.55 * cos(u * 2.0)) * cos(spireT * 1.5),
          (uv.y - 0.5) * 4.6 + 0.45 * sin(u * 2.0),
          (spireR + 0.55 * cos(u * 2.0)) * sin(spireT * 1.5)
        );
        vec3 n3 = normalize(vec3(cos(spireT * 1.5), 0.25, sin(spireT * 1.5)));

        pos = p0 * uTopoWeights.x + p1 * uTopoWeights.y + p2 * uTopoWeights.z + p3 * uTopoWeights.w;
        norm = normalize(n0 * uTopoWeights.x + n1 * uTopoWeights.y + n2 * uTopoWeights.z + n3 * uTopoWeights.w);
      }

      void main() {
        vUv = uv;

        vec3 basePos, baseNorm;
        evalTopologies(uv, basePos, baseNorm);

        // Sample live Gray-Scott concentration V from tiled GPU texture
        vec2 tiledUv = vec2(uv.x * 2.0, uv.y * 2.0);
        vec4 chem = texture2D(uChemTex, tiledUv);
        float V = chem.g;
        vChemV = V;

        // Smooth organic ridge profile + micro-pulsation
        float ridge = smoothstep(0.08, 0.88, V);
        float pulse = 1.0 + 0.05 * sin(uTime * 2.5 + V * 8.0);
        vec3 displacedPos = basePos + baseNorm * (ridge * uExtrude * pulse);

        vec4 worldPos = modelMatrix * vec4(displacedPos, 1.0);
        vWorldPos = worldPos.xyz;
        vBaseNormal = normalize(mat3(modelMatrix) * baseNorm);

        gl_Position = projectionMatrix * viewMatrix * worldPos;
      }
    `;

    const fragmentShader = `
      uniform sampler2D uChemTex;
      uniform float uTime;
      uniform float uExtrude;
      uniform int uShaderMode;

      varying vec2 vUv;
      varying vec3 vWorldPos;
      varying vec3 vBaseNormal;
      varying float vChemV;

      void main() {
        vec2 tiledUv = vec2(vUv.x * 2.0, vUv.y * 2.0);
        vec4 chem = texture2D(uChemTex, tiledUv);
        float U = chem.r;
        float V = chem.g;

        // Compute true 3D sculpted surface normal using screen-space derivatives of displaced geometry
        vec3 dpdx = dFdx(vWorldPos);
        vec3 dpdy = dFdy(vWorldPos);
        vec3 geomNormal = normalize(cross(dpdx, dpdy));
        vec3 N = normalize(mix(vBaseNormal, geomNormal, 0.78));

        vec3 Vdir = normalize(cameraPosition - vWorldPos);
        vec3 L1 = normalize(vec3(6.0, 10.0, 8.0));
        vec3 L2 = normalize(vec3(-7.0, -5.0, 5.0));
        vec3 H1 = normalize(L1 + Vdir);

        float diff1 = max(dot(N, L1), 0.0);
        float diff2 = max(dot(N, L2), 0.0);
        float spec = pow(max(dot(N, H1), 0.0), 48.0);
        float fresnel = pow(1.0 - max(dot(N, Vdir), 0.0), 3.0);

        float ridge = smoothstep(0.10, 0.85, V);
        float edgeGlow = smoothstep(0.18, 0.45, V) * (1.0 - smoothstep(0.45, 0.82, V));

        vec3 finalColor;

        if (uShaderMode == 0) {
          // THEME 0: MOLTEN BASALT & SOLAR GOLD
          vec3 basalt = vec3(0.055, 0.042, 0.038) * (0.45 + 0.75 * diff1);
          vec3 magmaCrimson = vec3(0.92, 0.16, 0.06);
          vec3 solarGold = vec3(1.00, 0.78, 0.24);
          vec3 hotCore = vec3(1.00, 0.96, 0.78);

          vec3 activeColor = mix(magmaCrimson, solarGold, smoothstep(0.25, 0.75, V));
          activeColor = mix(activeColor, hotCore, smoothstep(0.70, 0.98, V));

          finalColor = mix(basalt, activeColor * (0.65 + 0.55 * diff1), ridge);
          finalColor += vec3(1.0, 0.42, 0.08) * edgeGlow * 0.55;
          finalColor += vec3(1.0, 0.82, 0.45) * spec * (0.25 + 0.75 * ridge);
          finalColor += vec3(1.0, 0.45, 0.12) * fresnel * 0.28;
        } else if (uShaderMode == 1) {
          // THEME 1: KINTSUGI ROYAL PORCELAIN & 24K METALLIC GOLD
          vec3 porcelain = vec3(0.94, 0.91, 0.86) * (0.38 + 0.68 * diff1 + 0.20 * diff2);
          vec3 cobalt = vec3(0.08, 0.24, 0.58);
          vec3 gold24k = vec3(0.98, 0.78, 0.22);

          vec3 vein = mix(cobalt, gold24k * (0.8 + 0.5 * diff1), smoothstep(0.28, 0.65, V));
          finalColor = mix(porcelain, vein, ridge);
          finalColor += vec3(1.0, 0.92, 0.65) * spec * 0.85;
          finalColor += vec3(0.95, 0.75, 0.25) * edgeGlow * 0.45;
        } else {
          // THEME 2: CYBER-CHROME IRIDESCENT CHITIN
          vec3 irid = 0.5 + 0.5 * cos(6.28318 * (vec3(0.0, 0.33, 0.67) + V * 1.1 + dot(N, Vdir) * 0.65));
          vec3 darkMetal = vec3(0.08, 0.09, 0.12) * (0.4 + 0.7 * diff1);
          finalColor = mix(darkMetal, irid * (0.55 + 0.65 * diff1), ridge);
          finalColor += vec3(0.95, 0.98, 1.0) * spec * 1.15;
          finalColor += irid * fresnel * 0.55;
        }

        gl_FragColor = vec4(finalColor, 1.0);
      }
    `;

    // High-Resolution 168x168 Parametric Grid (56,448 triangles)
    const manifoldGeo = new THREE.PlaneGeometry(1, 1, 168, 168);
    const manifoldMat = new THREE.ShaderMaterial({
      uniforms: morphUniforms,
      vertexShader,
      fragmentShader,
      side: THREE.DoubleSide
    });

    const sculptureGroup = new THREE.Group();
    const manifoldMesh = new THREE.Mesh(manifoldGeo, manifoldMat);
    sculptureGroup.add(manifoldMesh);
    scene.add(sculptureGroup);

    // Ambient Floating Golden Spores / Catalyst Motes
    const sporeCount = 450;
    const sporeGeo = new THREE.BufferGeometry();
    const sporePos = new Float32Array(sporeCount * 3);
    for (let i = 0; i < sporeCount; i++) {
      const r = 2.8 + Math.random() * 2.2;
      const t = Math.random() * Math.PI * 2;
      const p = Math.acos(2 * Math.random() - 1);
      sporePos[i * 3]     = r * Math.sin(p) * Math.cos(t);
      sporePos[i * 3 + 1] = r * Math.cos(p);
      sporePos[i * 3 + 2] = r * Math.sin(p) * Math.sin(t);
    }
    sporeGeo.setAttribute('position', new THREE.BufferAttribute(sporePos, 3));
    const sporeMesh = new THREE.Points(sporeGeo, new THREE.PointsMaterial({
      color: 0xffb84d,
      size: 0.045,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending
    }));
    sculptureGroup.add(sporeMesh);

    // =========================================================================
    // 5. WSL UBUNTU TELEMETRY BRIDGE & UI CONTROLS
    // =========================================================================
    let teleTimer = null;
    function sendTelemetry(eventLabel = "PDE_UPDATE") {
      if (teleTimer) clearTimeout(teleTimer);
      teleTimer = setTimeout(() => {
        fetch('/api/telemetry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event: eventLabel,
            regime: state.regime,
            F: state.F,
            k: state.k,
            meanV: state.meanV,
            entropy: state.entropy,
            steps: state.totalSteps
          })
        }).catch(() => {});
      }, 100);
    }

    sendTelemetry("INITIALIZE_TURING_OS");

    // Smooth 3D Topology Morph Target Weights
    const targetTopoWeights = new THREE.Vector4(1, 0, 0, 0);
    document.querySelectorAll('[data-topo]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-topo]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const idx = parseInt(btn.dataset.topo, 10);
        state.topology = idx;
        targetTopoWeights.set(
          idx === 0 ? 1 : 0,
          idx === 1 ? 1 : 0,
          idx === 2 ? 1 : 0,
          idx === 3 ? 1 : 0
        );
        sendTelemetry(`MORPH_TOPOLOGY_${idx}`);
      });
    });

    // 5 Gray-Scott Reaction Regimes
    const REGIMES = {
      coral:   { F: 0.0290, k: 0.0570 },
      mitosis: { F: 0.0367, k: 0.0649 },
      spirals: { F: 0.0180, k: 0.0510 },
      spots:   { F: 0.0350, k: 0.0600 },
      worms:   { F: 0.0540, k: 0.0630 }
    };

    document.querySelectorAll('[data-regime]').forEach(item => {
      item.addEventListener('click', () => {
        document.querySelectorAll('[data-regime]').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
        const rName = item.dataset.regime;
        state.regime = rName;
        state.F = REGIMES[rName].F;
        state.k = REGIMES[rName].k;

        document.getElementById('slFeed').value = state.F;
        document.getElementById('lblFeed').textContent = state.F.toFixed(4);
        document.getElementById('slKill').value = state.k;
        document.getElementById('lblKill').textContent = state.k.toFixed(4);

        seedReactionField(false);
        sendTelemetry(`REGIME_${rName.toUpperCase()}`);
      });
    });

    // Material Shader Switcher
    document.querySelectorAll('[data-shader]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-shader]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.shaderMode = parseInt(btn.dataset.shader, 10);
        morphUniforms.uShaderMode.value = state.shaderMode;
        sendTelemetry(`SHADER_MODE_${state.shaderMode}`);
      });
    });

    // Bottom Console Buttons
    const btnToggleSpin = document.getElementById('btnToggleSpin');
    btnToggleSpin.addEventListener('click', () => {
      state.spinning = !state.spinning;
      btnToggleSpin.textContent = state.spinning ? '⏸ Spin' : '▶ Spin';
      btnToggleSpin.classList.toggle('active', state.spinning);
    });

    document.getElementById('btnReverseSpin').addEventListener('click', () => {
      state.spinDir *= -1;
    });

    const btnTumble = document.getElementById('btnTumble');
    btnTumble.addEventListener('click', () => {
      state.tumble = !state.tumble;
      btnTumble.classList.toggle('active', state.tumble);
      if (!state.tumble) {
        sculptureGroup.rotation.x = 0;
        sculptureGroup.rotation.z = 0;
      }
    });

    document.getElementById('btnMitosisWave').addEventListener('click', () => {
      seedReactionField(false);
      sendTelemetry("CATALYST_WAVE_INJECTED");
    });

    document.getElementById('btnSeedBurst').addEventListener('click', () => {
      seedReactionField(false);
      sendTelemetry("CATALYST_DROP_INJECTED");
    });

    document.getElementById('btnClearField').addEventListener('click', () => {
      seedReactionField(true);
      sendTelemetry("SUBSTRATE_RESET");
    });

    let camTarget = null;
    function moveCam(x, y, z) { camTarget = new THREE.Vector3(x, y, z); }
    document.getElementById('camFront').addEventListener('click', () => moveCam(0, 1.2, 9.2));
    document.getElementById('camTop').addEventListener('click', () => moveCam(0, 9.5, 0.01));
    document.getElementById('camClose').addEventListener('click', () => moveCam(0, 0.8, 5.4));
    document.getElementById('btnCinema').addEventListener('click', () => document.body.classList.toggle('ui-hidden'));

    // Bind Sliders
    document.getElementById('slExtrude').addEventListener('input', (e) => {
      state.extrude = parseFloat(e.target.value);
      morphUniforms.uExtrude.value = state.extrude;
      document.getElementById('lblExtrude').textContent = state.extrude.toFixed(2);
    });

    document.getElementById('slFeed').addEventListener('input', (e) => {
      state.F = parseFloat(e.target.value);
      document.getElementById('lblFeed').textContent = state.F.toFixed(4);
      sendTelemetry("SLIDER_FEED_F");
    });

    document.getElementById('slKill').addEventListener('input', (e) => {
      state.k = parseFloat(e.target.value);
      document.getElementById('lblKill').textContent = state.k.toFixed(4);
      sendTelemetry("SLIDER_KILL_K");
    });

    document.getElementById('slSpin').addEventListener('input', (e) => {
      state.spinSpeed = parseFloat(e.target.value);
      document.getElementById('lblSpin').textContent = `${state.spinSpeed.toFixed(2)} rad/s`;
    });

    document.getElementById('slSubsteps').addEventListener('input', (e) => {
      state.substeps = parseInt(e.target.value, 10);
      document.getElementById('lblSubsteps').textContent = `${state.substeps}x`;
    });

    document.getElementById('slBloom').addEventListener('input', (e) => {
      bloomPass.strength = parseFloat(e.target.value);
      document.getElementById('lblBloom').textContent = bloomPass.strength.toFixed(2);
    });

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') { e.preventDefault(); btnToggleSpin.click(); }
      else if (e.key === 'h' || e.key === 'H') document.body.classList.toggle('ui-hidden');
    });

    // =========================================================================
    // 6. MAIN 60FPS PDE + 3D MORPHOGENESIS ANIMATION LOOP
    // =========================================================================
    const clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      const dt = Math.min(clock.getDelta(), 0.05);
      const elapsed = clock.getElapsedTime();

      // Advance Coupled Gray-Scott PDE Substeps
      for (let s = 0; s < state.substeps; s++) {
        stepGrayScottPDE();
      }
      syncTextureAnd2DCanvas();

      morphUniforms.uTime.value = elapsed;

      // Smoothly interpolate 3D manifold topology weights
      morphUniforms.uTopoWeights.value.lerp(targetTopoWeights, dt * 4.5);

      // Rotate 3D Sculpture
      if (state.spinning) {
        sculptureGroup.rotation.y += dt * state.spinSpeed * state.spinDir;
        if (state.tumble) {
          sculptureGroup.rotation.x = Math.sin(elapsed * 0.55) * 0.48;
          sculptureGroup.rotation.z = Math.cos(elapsed * 0.40) * 0.38;
        }
      }

      if (camTarget) {
        camera.position.lerp(camTarget, dt * 5.0);
        controls.target.lerp(new THREE.Vector3(0, 0, 0), dt * 5.0);
        if (camera.position.distanceTo(camTarget) < 0.08) camTarget = null;
      }

      controls.update();
      composer.render();
    }

    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      composer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
"""


class TuringMorphogenesisHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(HTML_PAYLOAD.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/telemetry":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(raw)
                ts = time.strftime("%H:%M:%S")
                ev = data.get("event", "PDE_STEP")
                regime = data.get("regime", "coral").upper()
                f_val = data.get("F", 0.029)
                k_val = data.get("k", 0.057)
                mean_v = data.get("meanV", 0.28)
                ent = data.get("entropy", 3.82)
                steps = data.get("steps", 0)

                print(
                    f"{DIM}[{ts}]{RESET} "
                    f"{ORANGE}{BOLD}[TURING-PDE]{RESET} "
                    f"Event={GOLD}{ev:<22}{RESET} | "
                    f"Regime={CRIMSON}{regime:<8}{RESET} | "
                    f"F={f_val:<6.4f} k={k_val:<6.4f} | "
                    f"⟨V⟩={GOLD}{mean_v:<5.3f}{RESET} | "
                    f"Entropy={GREEN}{ent:<4.2f} bits{RESET} | "
                    f"Steps={WHITE}{steps}{RESET}",
                    flush=True,
                )
            except Exception:
                pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def find_free_port(start_port=8090):
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def open_browser_from_wsl(url):
    time.sleep(0.8)
    try:
        with open("/proc/version", "r") as f:
            proc_ver = f.read().lower()
        if "microsoft" in proc_ver or "wsl" in proc_ver:
            subprocess.Popen(
                ["cmd.exe", "/c", "start", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
    except Exception:
        pass

    try:
        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def main():
    port = find_free_port(8090)
    url = f"http://localhost:{port}"

    os.system("clear" if os.name == "posix" else "cls")
    print(f"{ORANGE}{BOLD}" + "=" * 92 + f"{RESET}")
    print(
        f"{GOLD}{BOLD}   TURING-OS // 3D MORPHOGENESIS & REACTION-DIFFUSION ENGINE (WSL UBUNTU EDITION){RESET}"
    )
    print(
        f"{DIM}   Coupled Gray-Scott PDEs: ∂t(U) = Du∇²U - UV² + F(1-U) ,  ∂t(V) = Dv∇²V + UV² - (F+k)V{RESET}"
    )
    print(f"{ORANGE}{BOLD}" + "=" * 92 + f"{RESET}")
    print(
        f" {GREEN}✔{RESET} {BOLD}WSL Ubuntu Turing-OS Server Active:{RESET}   {GOLD}{BOLD}{url}{RESET}"
    )
    print(
        f" {GREEN}✔{RESET} {BOLD}VS Code Quick Open:{RESET}                  {ORANGE}Ctrl + Click{RESET} the link above"
    )
    print(
        f" {GREEN}✔{RESET} {BOLD}Stop Server:{RESET}                         Press {CRIMSON}Ctrl + C{RESET} in this Ubuntu terminal"
    )
    print(f"{ORANGE}" + "-" * 92 + f"{RESET}")
    print(f"{BOLD} LIVE GRAY-SCOTT REACTION-DIFFUSION TELEMETRY STREAM:{RESET}")

    threading.Thread(target=open_browser_from_wsl, args=(url,), daemon=True).start()

    server = http.server.ThreadingHTTPServer(
        ("0.0.0.0", port), TuringMorphogenesisHandler
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(
            f"\n{CRIMSON}[TURING-OS STOPPED]{RESET} Shutting down 3D Morphogenesis Engine."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
