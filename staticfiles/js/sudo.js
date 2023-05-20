    // создаем объект Swiper и настраиваем его
    var mySwiper = new Swiper('.swiper-container', {
      slidesPerView: window.innerWidth <= 670 ?1 :window.innerWidth <= 990 ?2 :3, /* показываем сразу 3 слайда */
      spaceBetween: 30,
      loop: false, /* включаем бесконечный скролл */
      autoHeight: true,
      centeredSlides: true, /* делаем активный слайд по центру */
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true, /* делаем точки навигации кликабельными */
      },
    });

    // добавляем обработчик события click для слайдов
    const slides = document.querySelectorAll('.swiper-slide');
    slides.forEach((item, index) => {
        item.setAttribute('data-swiper-slide-index', index)
    })


