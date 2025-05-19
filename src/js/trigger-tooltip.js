let glossaryData = null;

async function loadGlossaryData() {
  if (glossaryData === null) {
    try {
      const response = await fetch("/glossary.json");
      if (!response.ok) throw new Error("fail to load glossary.json");
      glossaryData = await response.json();
    } catch (error) {
      console.error("fail to load glossary.json:", error);
      glossaryData = [];
    }
  }
}

function replaceTag(element) {
  const matched = glossaryData.find((item) => item.term.includes(element.textContent.trim()));

  const container = document.createElement("div");
  container.className = "trigger-container";
  container.innerHTML = `<span class="hover-trigger">${
    element.innerHTML
  }</span><div class="tooltip">${matched?.description || "There is no description."}</div>`;

  element.replaceWith(container);

  return container;
}

function initTooltip(container) {
  const trigger = container.querySelector(".hover-trigger");
  const tooltip = container.querySelector(".tooltip");

  let hideTimer, showTimer;
  const showDelay = 500;

  const updatePosition = () => {
    const triggerRect = trigger.getBoundingClientRect();

    const leftPos = triggerRect.left + triggerRect.width / 2 - tooltip.offsetWidth / 2;
    const rightEdge = leftPos + tooltip.offsetWidth;

    if (leftPos < 100) {
      tooltip.style.left = `${100 - triggerRect.left}px`;
      tooltip.style.right = "auto";
      tooltip.style.transform = "none";
    } else if (rightEdge > window.innerWidth - 100) {
      tooltip.style.left = "auto";
      tooltip.style.right = `${triggerRect.right + 100 - window.innerWidth}px`;
      tooltip.style.transform = "none";
    } else {
      tooltip.style.left = "50%";
      tooltip.style.right = "auto";
      tooltip.style.transform = "translateX(-50%)";
    }
  };

  trigger.addEventListener("mouseenter", () => {
    clearTimeout(hideTimer);
    clearTimeout(showTimer);
    updatePosition();
    showTimer = setTimeout(() => {
      tooltip.classList.add("active");
    }, showDelay);
  });

  trigger.addEventListener("mouseleave", () => {
    clearTimeout(showTimer);
    hideTimer = setTimeout(() => {
      tooltip.classList.remove("active");
    }, 200);
  });

  tooltip.addEventListener("mouseenter", () => {
    clearTimeout(hideTimer);
    if (!tooltip.classList.contains("active")) {
      tooltip.classList.add("active");
    }
  });

  tooltip.addEventListener("mouseleave", () => {
    hideTimer = setTimeout(() => {
      tooltip.classList.remove("active");
    }, 200);
  });
}
