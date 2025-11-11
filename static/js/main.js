document.addEventListener('DOMContentLoaded', () => {
  const contentArea = document.getElementById('post-content');
  if (!contentArea) return;

  const paragraphs = Array.from(contentArea.querySelectorAll('p')).filter(p => p.querySelectorAll('img').length > 1);

  paragraphs.forEach(p => {
    const imgs = Array.from(p.querySelectorAll('img'));
    if (imgs.length < 2) return;
    insertCarousel(imgs, p);
  });
});

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

