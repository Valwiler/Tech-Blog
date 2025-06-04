// class ThemeManager {
//   constructor() {
//     this.theme = this.getStoredTheme() || this.getSystemTheme();
//     this.themeToggle = null;
//     this.init();
//   }

//   init() {
//     // Apply stored theme
//     this.applyTheme(this.theme);

//     // Create theme toggle button
//     this.createThemeToggle();

//     // Listen for system theme changes
//     this.watchSystemTheme();
//   }

//   getStoredTheme() {
//     return localStorage.getItem('theme');
//   }

//   getSystemTheme() {
//     return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
//   }

//   setStoredTheme(theme) {
//     localStorage.setItem('theme', theme);
//   }

//   applyTheme(theme) {
//     document.documentElement.setAttribute('data-theme', theme);
//     this.theme = theme;
//     this.setStoredTheme(theme);

//     // Update toggle state
//     if (this.themeToggle) {
//       const icon = this.themeToggle.querySelector('.theme-icon');
//       const announcement = this.themeToggle.querySelector('.theme-toggle-announcement');

//       icon.textContent = theme === 'dark' ? '☀️' : '🌙';
//       icon.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');

//       if (announcement) {
//         announcement.textContent = `Switched to ${theme} theme`;
//       }

//       // Add transition class for animation
//       this.themeToggle.classList.add('theme-transitioning');
//       setTimeout(() => {
//         this.themeToggle.classList.remove('theme-transitioning');
//       }, 600);
//     }
//   }

//   createThemeToggle() {
//     this.themeToggle = document.createElement('button');
//     this.themeToggle.className = 'theme-toggle';
//     this.themeToggle.setAttribute('aria-label', 'Toggle theme');
//     this.themeToggle.setAttribute('title', 'Toggle theme');

//     const currentIcon = this.theme === 'dark' ? '☀️' : '🌙';

//     this.themeToggle.innerHTML = `
//       <div class="theme-switch">
//         <div class="theme-handle">
//           <span class="theme-icon" role="img" aria-label="${this.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}">${currentIcon}</span>
//         </div>
//       </div>
//       <span class="theme-toggle-announcement" aria-live="polite" aria-atomic="true"></span>
//     `;

//     this.themeToggle.addEventListener('click', () => {
//       const newTheme = this.theme === 'dark' ? 'light' : 'dark';
//       this.applyTheme(newTheme);
//     });

//     document.body.appendChild(this.themeToggle);
//   }

//   watchSystemTheme() {
//     const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

//     mediaQuery.addEventListener('change', (e) => {
//       if (!this.getStoredTheme()) {
//         this.applyTheme(e.matches ? 'dark' : 'light');
//       }
//     });
//   }
// }

// // Mobile Menu Toggle
// class MobileMenu {
//   constructor() {
//     this.menu = document.querySelector('.main-menu');
//     this.toggle = document.querySelector('.menu-toggle');
//     this.backdrop = document.querySelector('.menu-backdrop');
//     this.isOpen = false;

//     if (this.toggle && this.menu) {
//       this.init();
//     }
//   }

//   init() {
//     this.toggle.addEventListener('click', () => this.toggleMenu());

//     if (this.backdrop) {
//       this.backdrop.addEventListener('click', () => this.closeMenu());
//     }

//     // Close menu on escape key
//     document.addEventListener('keydown', (e) => {
//       if (e.key === 'Escape' && this.isOpen) {
//         this.closeMenu();
//       }
//     });

//     // Handle submenu toggles
//     this.handleSubmenus();

//     // Close menu when clicking menu items on mobile
//     const menuLinks = this.menu.querySelectorAll('a');
//     menuLinks.forEach(link => {
//       link.addEventListener('click', () => {
//         if (window.innerWidth <= 1024) {
//           this.closeMenu();
//         }
//       });
//     });
//   }

//   toggleMenu() {
//     if (this.isOpen) {
//       this.closeMenu();
//     } else {
//       this.openMenu();
//     }
//   }

//   openMenu() {
//     this.menu.classList.add('active');
//     this.toggle.classList.add('active');
//     if (this.backdrop) this.backdrop.classList.add('active');
//     document.body.style.overflow = 'hidden';
//     this.toggle.setAttribute('aria-expanded', 'true');
//     this.isOpen = true;

//     // Focus management
//     const firstMenuItem = this.menu.querySelector('a');
//     if (firstMenuItem) {
//       firstMenuItem.focus();
//     }
//   }

//   closeMenu() {
//     this.menu.classList.remove('active');
//     this.toggle.classList.remove('active');
//     if (this.backdrop) this.backdrop.classList.remove('active');
//     document.body.style.overflow = '';
//     this.toggle.setAttribute('aria-expanded', 'false');
//     this.isOpen = false;

//     // Return focus to toggle button
//     this.toggle.focus();
//   }

//   handleSubmenus() {
//     const submenuParents = this.menu.querySelectorAll('li');

//     submenuParents.forEach(parent => {
//       const submenu = parent.querySelector('.submenu');
//       if (submenu) {
//         parent.classList.add('has-submenu');
//         const link = parent.querySelector('> a');

//         // Add dropdown indicator
//         const indicator = document.createElement('span');
//         indicator.className = 'submenu-indicator';
//         indicator.setAttribute('aria-hidden', 'true');
//         link.appendChild(indicator);

//         link.addEventListener('click', (e) => {
//           if (window.innerWidth <= 1024) {
//             e.preventDefault();
//             parent.classList.toggle('active');

//             // Update aria-expanded
//             const isExpanded = parent.classList.contains('active');
//             link.setAttribute('aria-expanded', isExpanded);
//           }
//         });
//       }
//     });
//   }
// }

// // Gallery Lightbox
// class GalleryLightbox {
//   constructor() {
//     this.galleries = document.querySelectorAll('.gallery-images');
//     this.lightbox = null;
//     this.currentIndex = 0;
//     this.images = [];
//     this.focusTrap = null;

//     if (this.galleries.length > 0) {
//       this.init();
//     }
//   }

//   init() {
//     this.createLightbox();

//     this.galleries.forEach(gallery => {
//       const images = gallery.querySelectorAll('.gallery-image');

//       images.forEach((image, index) => {
//         image.addEventListener('click', () => {
//           this.images = Array.from(images).map(img => ({
//             src: img.querySelector('img').src,
//             alt: img.querySelector('img').alt
//           }));
//           this.openLightbox(index);
//         });

//         // Keyboard accessibility
//         image.addEventListener('keydown', (e) => {
//           if (e.key === 'Enter' || e.key === ' ') {
//             e.preventDefault();
//             this.images = Array.from(images).map(img => ({
//               src: img.querySelector('img').src,
//               alt: img.querySelector('img').alt
//             }));
//             this.openLightbox(index);
//           }
//         });
//       });
//     });
//   }

//   createLightbox() {
//     this.lightbox = document.createElement('div');
//     this.lightbox.className = 'gallery-lightbox';
//     this.lightbox.setAttribute('role', 'dialog');
//     this.lightbox.setAttribute('aria-modal', 'true');
//     this.lightbox.setAttribute('aria-label', 'Image gallery viewer');

//     this.lightbox.innerHTML = `
//       <button class="lightbox-close" aria-label="Close gallery">×</button>
//       <button class="lightbox-nav prev" aria-label="Previous image">‹</button>
//       <button class="lightbox-nav next" aria-label="Next image">›</button>
//       <figure class="lightbox-content">
//         <img src="" alt="">
//         <figcaption class="lightbox-caption"></figcaption>
//       </figure>
//       <div class="lightbox-counter" aria-live="polite"></div>
//     `;

//     document.body.appendChild(this.lightbox);

//     // Event listeners
//     const close = this.lightbox.querySelector('.lightbox-close');
//     const prev = this.lightbox.querySelector('.prev');
//     const next = this.lightbox.querySelector('.next');

//     close.addEventListener('click', () => this.closeLightbox());
//     prev.addEventListener('click', () => this.navigateImage(-1));
//     next.addEventListener('click', () => this.navigateImage(1));

//     this.lightbox.addEventListener('click', (e) => {
//       if (e.target === this.lightbox) {
//         this.closeLightbox();
//       }
//     });

//     // Keyboard navigation
//     document.addEventListener('keydown', (e) => {
//       if (!this.lightbox.classList.contains('active')) return;

//       switch(e.key) {
//         case 'Escape':
//           this.closeLightbox();
//           break;
//         case 'ArrowLeft':
//           this.navigateImage(-1);
//           break;
//         case 'ArrowRight':
//           this.navigateImage(1);
//           break;
//       }
//     });
//   }

//   openLightbox(index) {
//     this.currentIndex = index;
//     this.updateImage();
//     this.lightbox.classList.add('active');
//     document.body.style.overflow = 'hidden';

//     // Focus management
//     this.focusTrap = this.lightbox.querySelector('.lightbox-close');
//     this.focusTrap.focus();
//   }

//   closeLightbox() {
//     this.lightbox.classList.remove('active');
//     document.body.style.overflow = '';

//     // Return focus to the original image
//     const galleries = document.querySelectorAll('.gallery-images');
//     galleries.forEach(gallery => {
//       const images = gallery.querySelectorAll('.gallery-image');
//       if (images[this.currentIndex]) {
//         images[this.currentIndex].focus();
//       }
//     });
//   }

//   navigateImage(direction) {
//     this.currentIndex += direction;

//     if (this.currentIndex < 0) {
//       this.currentIndex = this.images.length - 1;
//     } else if (this.currentIndex >= this.images.length) {
//       this.currentIndex = 0;
//     }

//     this.updateImage();
//   }

//   updateImage() {
//     const img = this.lightbox.querySelector('img');
//     const caption = this.lightbox.querySelector('.lightbox-caption');
//     const counter = this.lightbox.querySelector('.lightbox-counter');

//     const currentImage = this.images[this.currentIndex];
//     img.src = currentImage.src;
//     img.alt = currentImage.alt;
//     caption.textContent = currentImage.alt;
//     counter.textContent = `${this.currentIndex + 1} / ${this.images.length}`;
//   }
// }

// // Code Block Copy Button
// class CodeCopyButton {
//   constructor() {
//     this.codeBlocks = document.querySelectorAll('.code-block');

//     if (this.codeBlocks.length > 0) {
//       this.init();
//     }
//   }

//   init() {
//     this.codeBlocks.forEach(block => {
//       const pre = block.querySelector('pre');
//       if (!pre) return;

//       const wrapper = document.createElement('div');
//       wrapper.className = 'code-block-wrapper';

//       const button = document.createElement('button');
//       button.className = 'code-copy-button';
//       button.textContent = 'Copy';
//       button.setAttribute('aria-label', 'Copy code to clipboard');

//       button.addEventListener('click', () => this.copyCode(pre, button));

//       wrapper.appendChild(button);
//       block.appendChild(wrapper);
//     });
//   }

//   async copyCode(pre, button) {
//     const code = pre.textContent;

//     try {
//       await navigator.clipboard.writeText(code);
//       button.textContent = 'Copied!';
//       button.classList.add('copied');

//       setTimeout(() => {
//         button.textContent = 'Copy';
//         button.classList.remove('copied');
//       }, 2000);
//     } catch (err) {
//       console.error('Failed to copy:', err);
//       button.textContent = 'Error';

//       setTimeout(() => {
//         button.textContent = 'Copy';
//       }, 2000);
//     }
//   }
// }

// // Smooth Scroll for Anchor Links
// class SmoothScroll {
//   constructor() {
//     this.init();
//   }

//   init() {
//     document.addEventListener('click', (e) => {
//       const link = e.target.closest('a[href^="#"]');

//       if (link) {
//         const targetId = link.getAttribute('href');
//         const target = document.querySelector(targetId);

//         if (target) {
//           e.preventDefault();

//           const header = document.querySelector('header');
//           const offset = header ? header.offsetHeight + 20 : 80;
//           const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;

//           window.scrollTo({
//             top: targetPosition,
//             behavior: 'smooth'
//           });

//           // Update URL without jumping
//           history.pushState(null, null, targetId);

//           // Set focus for accessibility
//           target.setAttribute('tabindex', '-1');
//           target.focus();
//         }
//       }
//     });
//   }
// }

// // Heading Anchors
// class HeadingAnchors {
//   constructor() {
//     this.headings = document.querySelectorAll('.heading-block, h1, h2, h3, h4, h5, h6');

//     if (this.headings.length > 0) {
//       this.init();
//     }
//   }

//   init() {
//     this.headings.forEach(heading => {
//       // Skip if already has an ID
//       if (!heading.id) {
//         // Create anchor ID from heading text
//         const text = heading.textContent.trim();
//         const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
//         heading.setAttribute('id', id);
//       }

//       // Add anchor link
//       const anchor = document.createElement('a');
//       anchor.className = 'heading-anchor';
//       anchor.href = `#${heading.id}`;
//       anchor.setAttribute('aria-label', 'Copy link to this section');
//       anchor.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg>';

//       anchor.addEventListener('click', async (e) => {
//         e.preventDefault();
//         const url = `${window.location.origin}${window.location.pathname}#${heading.id}`;

//         try {
//           await navigator.clipboard.writeText(url);
//           anchor.classList.add('copied');

//           // Show tooltip
//           const tooltip = document.createElement('span');
//           tooltip.className = 'heading-anchor-tooltip';
//           tooltip.textContent = 'Copied!';
//           anchor.appendChild(tooltip);

//           setTimeout(() => {
//             anchor.classList.remove('copied');
//             tooltip.remove();
//           }, 2000);

//           // Update URL
//           history.pushState(null, null, `#${heading.id}`);
//         } catch (err) {
//           console.error('Failed to copy URL:', err);
//         }
//       });

//       heading.appendChild(anchor);
//     });
//   }
// }

// // Intersection Observer for animations
// class AnimationObserver {
//   constructor() {
//     this.init();
//   }

//   init() {
//     const observerOptions = {
//       threshold: 0.1,
//       rootMargin: '0px 0px -100px 0px'
//     };

//     const observer = new IntersectionObserver((entries) => {
//       entries.forEach(entry => {
//         if (entry.isIntersecting) {
//           entry.target.classList.add('animate-in');
//           observer.unobserve(entry.target);
//         }
//       });
//     }, observerOptions);

//     // Observe all animatable elements
//     const animatableElements = document.querySelectorAll(`
//       .heading-block,
//       .paragraph-block,
//       .code-block,
//       .pull-quote-block,
//       .cta-block,
//       .image-gallery-block,
//       .embed-video-block,
//       .blog-card-block,
//       h1, h2, h3, h4, h5, h6,
//       .hero,
//       .footer-section
//     `);

//     animatableElements.forEach(element => {
//       observer.observe(element);
//     });
//   }
// }

// // Initialize all features when DOM is ready
// document.addEventListener('DOMContentLoaded', () => {
//   new ThemeManager();
//   new MobileMenu();
//   new GalleryLightbox();
//   new CodeCopyButton();
//   new SmoothScroll();
//   new HeadingAnchors();
//   new AnimationObserver();
// });


// // Theme management and interactive features

// Theme Toggle
class ThemeManager {
  constructor() {
    this.theme = this.getStoredTheme() || 'light';
    this.themeToggle = null;
    this.init();
  }

  init() {
    // Apply stored theme
    this.applyTheme(this.theme);

    // Create theme toggle button
    this.createThemeToggle();

    // Listen for system theme changes
    this.watchSystemTheme();
  }

  getStoredTheme() {
    return localStorage.getItem('theme');
  }

  setStoredTheme(theme) {
    localStorage.setItem('theme', theme);
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.theme = theme;
    this.setStoredTheme(theme);

    // Update toggle button icon
    if (this.themeToggle) {
      const icon = this.themeToggle.querySelector('.theme-icon');
      icon.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  createThemeToggle() {
    this.themeToggle = document.createElement('button');
    this.themeToggle.className = 'theme-toggle';
    this.themeToggle.setAttribute('aria-label', 'Toggle theme');
    this.themeToggle.innerHTML = `<span class="theme-icon">${this.theme === 'dark' ? '☀️' : '🌙'}</span>`;

    this.themeToggle.addEventListener('click', () => {
      const newTheme = this.theme === 'dark' ? 'light' : 'dark';
      this.applyTheme(newTheme);
    });

    document.body.appendChild(this.themeToggle);
  }

  watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    mediaQuery.addEventListener('change', (e) => {
      if (!this.getStoredTheme()) {
        this.applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
}


// Mobile Menu Toggle
class MobileMenu {
  constructor() {
    this.menu = document.querySelector('.main-menu');
    this.toggle = document.querySelector('.menu-toggle');
    this.backdrop = document.querySelector('.menu-backdrop');

    if (this.toggle && this.menu) {
      this.init();
    }
  }

  init() {
    this.toggle.addEventListener('click', () => this.toggleMenu());

    if (this.backdrop) {
      this.backdrop.addEventListener('click', () => this.closeMenu());
    }

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen()) {
        this.closeMenu();
      }
    });

    // Handle submenu toggles
    this.handleSubmenus();
  }

  toggleMenu() {
    const isOpen = this.isOpen();

    if (isOpen) {
      this.closeMenu();
    } else {
      this.openMenu();
    }
  }

  openMenu() {
    this.menu.classList.add('active');
    this.toggle.classList.add('active');
    if (this.backdrop) this.backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  closeMenu() {
    this.menu.classList.remove('active');
    this.toggle.classList.remove('active');
    if (this.backdrop) this.backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  isOpen() {
    return this.menu.classList.contains('active');
  }

  handleSubmenus() {
    const submenuParents = document.querySelectorAll('.main-menu > li.has-submenu');

    submenuParents.forEach(parent => {
      const link = parent.querySelector('a');

      link.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          parent.classList.toggle('active');
        }
      });
    });
  }
}

// Gallery Lightbox
class GalleryLightbox {
  constructor() {
    this.galleries = document.querySelectorAll('.gallery-images');
    this.lightbox = null;
    this.currentIndex = 0;
    this.images = [];

    if (this.galleries.length > 0) {
      this.init();
    }
  }

  init() {
    this.createLightbox();

    this.galleries.forEach(gallery => {
      const images = gallery.querySelectorAll('.gallery-image');

      images.forEach((image, index) => {
        image.addEventListener('click', () => {
          this.images = Array.from(images).map(img => img.querySelector('img').src);
          this.openLightbox(index);
        });

        // Make images keyboard accessible
        image.setAttribute('tabindex', '0');
        image.setAttribute('role', 'button');
        image.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.images = Array.from(images).map(img => img.querySelector('img').src);
            this.openLightbox(index);
          }
        });
      });
    });
  }

  createLightbox() {
    this.lightbox = document.createElement('div');
    this.lightbox.className = 'gallery-lightbox';
    this.lightbox.innerHTML = `
      <button class="lightbox-close" aria-label="Close lightbox">×</button>
      <button class="lightbox-nav prev" aria-label="Previous image">‹</button>
      <button class="lightbox-nav next" aria-label="Next image">›</button>
      <img src="" alt="Gallery image">
    `;

    document.body.appendChild(this.lightbox);

    // Event listeners
    const close = this.lightbox.querySelector('.lightbox-close');
    const prev = this.lightbox.querySelector('.prev');
    const next = this.lightbox.querySelector('.next');

    close.addEventListener('click', () => this.closeLightbox());
    prev.addEventListener('click', () => this.navigateImage(-1));
    next.addEventListener('click', () => this.navigateImage(1));

    this.lightbox.addEventListener('click', (e) => {
      if (e.target === this.lightbox) {
        this.closeLightbox();
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!this.lightbox.classList.contains('active')) return;

      switch(e.key) {
        case 'Escape':
          this.closeLightbox();
          break;
        case 'ArrowLeft':
          this.navigateImage(-1);
          break;
        case 'ArrowRight':
          this.navigateImage(1);
          break;
      }
    });
  }

  openLightbox(index) {
    this.currentIndex = index;
    this.updateImage();
    this.lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  closeLightbox() {
    this.lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  navigateImage(direction) {
    this.currentIndex += direction;

    if (this.currentIndex < 0) {
      this.currentIndex = this.images.length - 1;
    } else if (this.currentIndex >= this.images.length) {
      this.currentIndex = 0;
    }

    this.updateImage();
  }

  updateImage() {
    const img = this.lightbox.querySelector('img');
    img.src = this.images[this.currentIndex];
  }
}

// Code Block Copy Button
class CodeCopyButton {
  constructor() {
    this.codeBlocks = document.querySelectorAll('.code-block');

    if (this.codeBlocks.length > 0) {
      this.init();
    }
  }

  init() {
    this.codeBlocks.forEach(block => {
      const button = document.createElement('button');
      button.className = 'code-copy-button';
      button.textContent = 'Copy';
      button.setAttribute('aria-label', 'Copy code to clipboard');

      button.addEventListener('click', () => this.copyCode(block, button));

      block.appendChild(button);
    });
  }

  async copyCode(block, button) {
    const code = block.querySelector('pre').textContent;

    try {
      await navigator.clipboard.writeText(code);
      button.textContent = 'Copied!';
      button.classList.add('copied');

      setTimeout(() => {
        button.textContent = 'Copy';
        button.classList.remove('copied');
      }, 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
      button.textContent = 'Error';

      setTimeout(() => {
        button.textContent = 'Copy';
      }, 2000);
    }
  }
}

// Smooth Scroll for Anchor Links
class SmoothScroll {
  constructor() {
    this.init();
  }

  init() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]');

      if (link) {
        const targetId = link.getAttribute('href');
        const target = document.querySelector(targetId);

        if (target) {
          e.preventDefault();

          const offset = 80; // Header height
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      }
    });
  }
}

// Heading Anchors
class HeadingAnchors {
  constructor() {
    this.headings = document.querySelectorAll('.heading-block');

    if (this.headings.length > 0) {
      this.init();
    }
  }

  init() {
    this.headings.forEach(heading => {
      // Create anchor ID from heading text
      const text = heading.textContent.trim();
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');

      heading.setAttribute('id', id);

      // Add copy link button
      const anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = `#${id}`;
      anchor.setAttribute('aria-label', 'Copy link to this section');
      anchor.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg>';

      anchor.addEventListener('click', async (e) => {
        e.preventDefault();
        const url = `${window.location.origin}${window.location.pathname}#${id}`;

        try {
          await navigator.clipboard.writeText(url);
          anchor.classList.add('copied');

          setTimeout(() => {
            anchor.classList.remove('copied');
          }, 2000);
        } catch (err) {
          console.error('Failed to copy URL:', err);
        }
      });

      heading.appendChild(anchor);
    });
  }
}

// Initialize all features when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new ThemeManager();
  new MobileMenu();
  new GalleryLightbox();
  new CodeCopyButton();
  new SmoothScroll();
  new HeadingAnchors();

  // Add animate-in class to elements as they come into view
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all blocks
  const blocks = document.querySelectorAll('.heading-block, .paragraph-block, .code-block, .pull-quote-block, .cta-block, .image-gallery-block, .embed-video-block, .blog-card-block');

  blocks.forEach(block => {
    observer.observe(block);
  });
});
