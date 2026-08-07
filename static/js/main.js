document.addEventListener('DOMContentLoaded', () => {
  initCarousels();
  initPostNav();
});

function initCarousels() {
  const contentArea = document.getElementById('post-content');
  if (!contentArea) return;

  const paragraphs = Array.from(contentArea.querySelectorAll('p')).filter(p => p.querySelectorAll('img').length > 1);

  paragraphs.forEach(p => {
    const imgs = Array.from(p.querySelectorAll('img'));
    if (imgs.length < 2) return;
    insertCarousel(imgs, p);
  });
}

function initPostNav() {
  const nav = document.getElementById('post-nav');
  const content = document.getElementById('post-content');
  if (!nav || !content) return;

  const items = new Map();
  nav.querySelectorAll('.lecp-nav-item').forEach(item => {
    items.set(item.getAttribute('href').slice(1), item);
  });

  const headings = Array.from(content.querySelectorAll('h2')).filter(h => items.has(h.id));
  if (!headings.length || !('IntersectionObserver' in window)) return;

  const setActive = (id) => {
    items.forEach(item => item.classList.remove('is-active'));
    const item = items.get(id);
    if (item) item.classList.add('is-active');
  };

  const visible = new Set();

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        visible.add(entry.target.id);
      } else {
        visible.delete(entry.target.id);
      }
    });

    if (visible.size > 0) {
      const topMost = headings.find(h => visible.has(h.id));
      if (topMost) setActive(topMost.id);
      return;
    }

    const line = window.innerHeight * 0.2;
    let current = headings[0];
    for (const h of headings) {
      if (h.getBoundingClientRect().top < line) {
        current = h;
      } else {
        break;
      }
    }
    setActive(current.id);
  }, { rootMargin: '-20% 0px -70% 0px' });

  headings.forEach(h => observer.observe(h));
}

function insertCarousel(images, paragraph) {
  const swiperContainer = document.createElement('div');
  swiperContainer.className = 'swiper my-image-carousel';

  const swiperWrapper = document.createElement('div');
  swiperWrapper.className = 'swiper-wrapper';
  swiperContainer.appendChild(swiperWrapper);

  images.forEach(origImg => {
    const parent = origImg.parentNode.tagName === 'A' ? origImg.parentNode : origImg;
    const slide = document.createElement('div');
    slide.className = 'swiper-slide';
    slide.appendChild(parent.cloneNode(true));
    swiperWrapper.appendChild(slide);
  });

  const prev = document.createElement('div');
  prev.className = 'swiper-button-prev';
  const next = document.createElement('div');
  next.className = 'swiper-button-next';
  const pagination = document.createElement('div');
  pagination.className = 'swiper-pagination';
  swiperContainer.appendChild(prev);
  swiperContainer.appendChild(next);
  swiperContainer.appendChild(pagination);

  paragraph.parentNode.insertBefore(swiperContainer, paragraph);
  paragraph.remove();

  new Swiper(swiperContainer, {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 10,
    pagination: {
      el: swiperContainer.querySelector('.swiper-pagination'),
      clickable: true,
    },
    navigation: {
      nextEl: swiperContainer.querySelector('.swiper-button-next'),
      prevEl: swiperContainer.querySelector('.swiper-button-prev'),
    },
  });
}

