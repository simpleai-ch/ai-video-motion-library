(async()=>{
  const cfg=window.MOTION_CONFIG, opts=window.VIEWER;
  const viewport=document.querySelector('#viewport'), scene=document.querySelector('#scene'), video=document.querySelector('#video');
  const playButton=document.querySelector('#play'), replay=document.querySelector('#replay'), scrub=document.querySelector('#scrub'), clock=document.querySelector('#clock'), loop=document.querySelector('#loop');
  document.querySelector('#title').textContent=opts.title;
  let live=opts.engine==='browser'&&location.protocol!=='file:', playing=true, current=0, duration=cfg.duration_frames/cfg.fps, started=performance.now(), busy=false, lastFrame=-1, ready=false;
  scrub.max=duration;
  function display(){scrub.value=current;clock.textContent=`${current.toFixed(2)} / ${duration.toFixed(2)}s`;playButton.textContent=playing?'暂停':'播放'}
  function fit(){if(!live)return;const w=cfg.width,h=opts.stageHeight||cfg.height,s=Math.min(viewport.clientWidth/w,viewport.clientHeight/h);scene.style.width=w+'px';scene.style.height=h+'px';scene.style.transform=`translate(${(viewport.clientWidth-w*s)/2}px,${(viewport.clientHeight-h*s)/2}px) scale(${s})`}
  function setPlaying(value){playing=value;started=performance.now()-current*1000;if(!live){if(value)video.play().catch(()=>{});else video.pause()}display()}
  if(live){
    video.hidden=true;scene.hidden=false;scene.src='scene.html?render=1';fit();window.addEventListener('resize',fit);
    await new Promise(resolve=>scene.onload=resolve);
    while(!scene.contentWindow.MOTION_READY)await new Promise(r=>setTimeout(r,20));
    await scene.contentDocument.fonts.ready;ready=true;
  }else{
    scene.hidden=true;video.hidden=false;video.src=window.MOTION_OUTPUT||'preview.mp4';video.muted=true;video.playsInline=true;
    await new Promise((resolve,reject)=>{video.onloadedmetadata=resolve;video.onerror=reject});duration=video.duration;scrub.max=duration;ready=true;video.play().catch(()=>setPlaying(false));
    video.ontimeupdate=()=>{current=video.currentTime;display()};video.onended=()=>{if(loop.checked){video.currentTime=0;video.play()}else setPlaying(false)};
  }
  async function tick(now){
    if(live&&ready){
      if(playing){current=(now-started)/1000;if(current>=duration){if(loop.checked){current=0;started=now}else{current=duration;setPlaying(false)}}}
      const frame=Math.min(cfg.duration_frames-1,Math.floor(current*cfg.fps));
      if(frame!==lastFrame&&!busy){busy=true;try{const win=scene.contentWindow;if(win.seekFrame)await win.seekFrame(frame);else win.draw(cfg.time_unit==='seconds'?frame/cfg.fps:frame);lastFrame=frame}finally{busy=false}}
      display();
    }
    requestAnimationFrame(tick);
  }
  playButton.onclick=()=>setPlaying(!playing);replay.onclick=()=>{current=0;lastFrame=-1;if(!live)video.currentTime=0;setPlaying(true)};
  scrub.oninput=()=>{const target=Number(scrub.value);setPlaying(false);current=target;lastFrame=-1;if(!live)video.currentTime=current;display()};
  document.addEventListener('keydown',e=>{if(e.code==='Space'&&e.target.tagName!=='INPUT'){e.preventDefault();setPlaying(!playing)}});
  window.PREVIEW_READY=true;display();requestAnimationFrame(tick);
})().catch(error=>{document.querySelector('#title').textContent='预览载入失败：'+error.message;console.error(error)});
