//const menuTrigger = document.querySelector(".menu-trigger")
//const menuUl = document.querySelector("#header-nav-ul")
//
//
//menuTrigger.onclick = () => {
//    const displayState = menuUl.style.display
//    if (displayState === 'none') {
//        menuUl.style.display = 'block!important'
//        menuTrigger.addClass("active")
//    }
//    else {
//     menuUl.style.display = 'none!important'
//     menuTrigger.removeClass("active")
//    }
//}

 const menu = document.querySelector('.sideBarMenuIcon')
      const sideBar = document.querySelector('.sideBar')
      const sideBarMenu = document.querySelector('.sideBarMenu')

      menu.onclick = () => {
        const displayStatus = sideBarMenu.style.display
        if (displayStatus === 'none') {
          sideBar.style.height = '100vh'
          sideBar.style.background = 'gray'
          sideBarMenu.style.display = 'grid'
        } else {
          sideBar.style.height = 'auto'
          sideBar.style.background = 'transparent'
          sideBarMenu.style.display = 'none'
        }
      }