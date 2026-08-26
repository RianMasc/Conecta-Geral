(function(){
  const root=document.documentElement;
  if(localStorage.getItem('cg-large-font')==='1') root.classList.add('large-font');
  if(localStorage.getItem('cg-contrast')==='1') root.classList.add('high-contrast');
})();
function toggleFont(){const r=document.documentElement;r.classList.toggle('large-font');localStorage.setItem('cg-large-font',r.classList.contains('large-font')?'1':'0')}
function toggleContrast(){const r=document.documentElement;r.classList.toggle('high-contrast');localStorage.setItem('cg-contrast',r.classList.contains('high-contrast')?'1':'0')}
