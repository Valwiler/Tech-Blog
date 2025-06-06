// Table of Contents Generator
class TableOfContents {
  constructor() {
    this.tocContainer = document.getElementById('table-of-contents');
    this.contentArea = document.querySelector('.main-content');
    this.headings = [];
    this.tocLinks = [];
    this.activeHeading = null;
    this.scrollTimeout = null;

    if (this.tocContainer && this.contentArea) {
      this.init();
    }
  }

  init() {
    // Collect all headings
    this.collectHeadings();

    // Generate TOC
    this.generateTOC();

    // Set up observers and listeners
    this.setupIntersectionObserver();
    this.setupScrollListener();
    this.setupClickHandlers();

    // Set initial active state
    this.updateActiveHeading();
  }

  collectHeadings() {
    // Find all heading blocks (h2-h5)
    const headingElements = this.contentArea.querySelectorAll('.heading-block');

    this.headings = Array.from(headingElements).map((heading, index) => {
      // Create ID if it doesn't exist
      if (!heading.id) {
        const text = heading.textContent.trim();
        const id = this.generateId(text, index);
        heading.id = id;
      }

      // Get heading level from the tag name or class
      const level = this.getHeadingLevel(heading);

      return {
        element: heading,
        id: heading.id,
        text: heading.textContent.trim(),
        level: level,
        offset: 0
      };
    }).filter(h => h.level >= 2 && h.level <= 5); // Only include h2-h5
  }

  getHeadingLevel(element) {
    // Check if it's a heading block with size class
    const sizeMatch = element.className.match(/\bh(\d)\b/);
    if (sizeMatch) {
      return parseInt(sizeMatch[1]);
    }

    // Check the actual tag name
    const tagName = element.tagName.toLowerCase();
    if (tagName.match(/^h[1-6]$/)) {
      return parseInt(tagName.substring(1));
    }

    // Default to h2 if we can't determine
    return 2;
  }

  generateId(text, index) {
    // Convert text to a valid ID
    const baseId = text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '') // Remove special characters
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .replace(/-+/g, '-') // Replace multiple hyphens with single hyphen
      .trim();

    return baseId || `heading-${index}`;
  }

  generateTOC() {
    if (this.headings.length === 0) {
      this.tocContainer.style.display = 'none';
      return;
    }

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    let currentLevel = 2;
    let currentList = tocList;
    let listStack = [currentList];

    this.headings.forEach(heading => {
      // Adjust nesting based on heading level
      while (heading.level > currentLevel && currentLevel < 5) {
        const newList = document.createElement('ul');
        newList.className = 'toc-sublist';

        if (currentList.lastElementChild) {
          currentList.lastElementChild.appendChild(newList);
        } else {
          // Create a placeholder item if needed
          const placeholderItem = document.createElement('li');
          placeholderItem.className = 'toc-item';
          currentList.appendChild(placeholderItem);
          placeholderItem.appendChild(newList);
        }

        listStack.push(newList);
        currentList = newList;
        currentLevel++;
      }

      while (heading.level < currentLevel && listStack.length > 1) {
        listStack.pop();
        currentList = listStack[listStack.length - 1];
        currentLevel--;
      }

      // Create TOC item
      const listItem = document.createElement('li');
      listItem.className = 'toc-item';

      const link = document.createElement('a');
      link.href = `#${heading.id}`;
      link.className = 'toc-link';
      link.textContent = heading.text;
      link.setAttribute('data-level', heading.level);

      listItem.appendChild(link);
      currentList.appendChild(listItem);

      // Store reference to link
      this.tocLinks.push({
        element: link,
        headingId: heading.id,
        heading: heading
      });
    });

    // Create TOC header
    const tocHeader = document.createElement('div');
    tocHeader.className = 'toc-header';
    tocHeader.innerHTML = '<h3>On this page</h3>';

    // Add to container
    this.tocContainer.innerHTML = '';
    this.tocContainer.appendChild(tocHeader);
    this.tocContainer.appendChild(tocList);

    // Add progress indicator
    const progressBar = document.createElement('div');
    progressBar.className = 'toc-progress';
    progressBar.innerHTML = '<div class="toc-progress-bar"></div>';
    this.tocContainer.appendChild(progressBar);
  }

  setupIntersectionObserver() {
    const options = {
      rootMargin: '-20% 0% -70% 0%',
      threshold: [0, 0.5, 1]
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const heading = this.headings.find(h => h.element === entry.target);
        if (heading) {
          heading.isIntersecting = entry.isIntersecting;
          heading.intersectionRatio = entry.intersectionRatio;
        }
      });

      this.updateActiveHeading();
    }, options);

    this.headings.forEach(heading => {
      observer.observe(heading.element);
    });
  }

  setupScrollListener() {
    let ticking = false;

    const updateProgress = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPosition = window.scrollY;
      const progress = (scrollPosition / scrollHeight) * 100;

      const progressBar = this.tocContainer.querySelector('.toc-progress-bar');
      if (progressBar) {
        progressBar.style.width = `${progress}%`;
      }
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateProgress();
          this.updateHeadingOffsets();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Initial progress update
    updateProgress();
  }

  updateHeadingOffsets() {
    this.headings.forEach(heading => {
      const rect = heading.element.getBoundingClientRect();
      heading.offset = rect.top + window.scrollY;
    });
  }

  updateActiveHeading() {
    // Clear timeout if it exists
    if (this.scrollTimeout) {
      clearTimeout(this.scrollTimeout);
    }

    // Debounce the update
    this.scrollTimeout = setTimeout(() => {
      const scrollPosition = window.scrollY + 100; // Offset for better UX

      // Find the current active heading
      let activeHeading = null;

      // First, check intersecting headings
      const intersectingHeadings = this.headings.filter(h => h.isIntersecting);
      if (intersectingHeadings.length > 0) {
        activeHeading = intersectingHeadings[0];
      } else {
        // Fallback: find heading based on scroll position
        for (let i = this.headings.length - 1; i >= 0; i--) {
          if (scrollPosition >= this.headings[i].offset) {
            activeHeading = this.headings[i];
            break;
          }
        }
      }

      // Update active states
      this.tocLinks.forEach(link => {
        if (activeHeading && link.headingId === activeHeading.id) {
          link.element.classList.add('active');

          // Ensure the active link is visible in the TOC
          this.scrollTocToActive(link.element);
        } else {
          link.element.classList.remove('active');
        }
      });

      this.activeHeading = activeHeading;
    }, 10);
  }

  scrollTocToActive(activeLink) {
    const tocList = this.tocContainer.querySelector('.toc-list');
    const linkRect = activeLink.getBoundingClientRect();
    const listRect = tocList.getBoundingClientRect();

    if (linkRect.top < listRect.top || linkRect.bottom > listRect.bottom) {
      activeLink.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }
  }

  setupClickHandlers() {
    this.tocLinks.forEach(link => {
      link.element.addEventListener('click', (e) => {
        e.preventDefault();

        const targetId = link.headingId;
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
          // Calculate scroll position with offset for header
          const headerHeight = 100;
          const targetPosition = targetElement.offsetTop - headerHeight;

          // Smooth scroll to target
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });

          // Update URL without triggering scroll
          history.pushState(null, null, `#${targetId}`);

          // Manually trigger active state update after a delay
          setTimeout(() => {
            this.updateActiveHeading();
          }, 500);
        }
      });
    });

    // Handle mobile TOC toggle
    const tocToggle = document.getElementById('toc-toggle');
    if (tocToggle) {
      tocToggle.addEventListener('click', () => {
        this.tocContainer.classList.toggle('mobile-open');
        tocToggle.classList.toggle('active');
      });

      // Close TOC when clicking outside on mobile
      document.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024 &&
            !this.tocContainer.contains(e.target) &&
            !tocToggle.contains(e.target)) {
          this.tocContainer.classList.remove('mobile-open');
          tocToggle.classList.remove('active');
        }
      });
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new TableOfContents();
});
