const sections = document.querySelectorAll(".section");

const observer = new IntersectionObserver((entries)=>{
entries.forEach(entry=>{
if(entry.isIntersecting){
entry.target.classList.add("visible");
}
});
},{
threshold:0.15
});

sections.forEach(sec=>{
sec.classList.add("hidden");
observer.observe(sec);
});

// smooth scroll
document.querySelectorAll(".nav-links a").forEach(link=>{
link.addEventListener("click", e=>{
e.preventDefault();
document.querySelector(link.getAttribute("href"))
.scrollIntoView({behavior:"smooth"});
});
});

// active menu
const navLinks = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", ()=>{
let current = "";

```
document.querySelectorAll(".section").forEach(section=>{
    const sectionTop = section.offsetTop - 120;
    if(scrollY >= sectionTop){
        current = section.getAttribute("id");
    }
});

navLinks.forEach(link=>{
    link.classList.remove("active");
    if(link.getAttribute("href") === "#" + current){
        link.classList.add("active");
    }
});
```

});
