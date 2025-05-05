document.addEventListener("DOMContentLoaded", () => {
  // Auto-dismiss alerts after 5 seconds
  setTimeout(() => {
    const alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      const bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Function to update cart count badge
  function updateCartBadge(count) {
    const badge = document.querySelector('.cart-count-badge');
    if (badge) {
      if (count > 0) {
        badge.textContent = count;
        badge.style.display = '';
      } else {
        badge.style.display = 'none';
      }
    }
  }

  // Update cart count when adding/removing items
  document.addEventListener('click', (e) => {
    if (e.target.matches('[data-action="add-to-cart"]')) {
      const currentCount = parseInt(document.querySelector('.cart-count-badge')?.textContent || '0');
      updateCartBadge(currentCount + 1);
    } else if (e.target.matches('[data-action="remove-from-cart"]')) {
      const currentCount = parseInt(document.querySelector('.cart-count-badge')?.textContent || '0');
      if (currentCount > 0) {
        updateCartBadge(currentCount - 1);
      }
    }
  });

  // Handle address modal in checkout page
  const addAddressModal = document.getElementById("addAddressModal")
  if (addAddressModal) {
    addAddressModal.addEventListener("show.bs.modal", () => {
      fetch("/user/addresses/add/", {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.text())
        .then((html) => {
          document.getElementById("addressModalContent").innerHTML = html

          // Add event listener to the save button
          const saveBtn = document.getElementById("saveAddressBtn")
          if (saveBtn) {
            saveBtn.addEventListener("click", () => {
              const form = document.getElementById("addressModalForm")
              const formData = new FormData(form)

              fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                  "X-Requested-With": "XMLHttpRequest",
                },
              })
                .then((response) => response.json())
                .then((data) => {
                  if (data.success) {
                    window.location.reload()
                  }
                })
            })
          }
        })
    })
  }

  // Handle AJAX forms
  document.querySelectorAll("[data-ajax-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault()

      const formData = new FormData(form)

      fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Close any open modals
            const openModals = document.querySelectorAll(".modal.show")
            openModals.forEach((modal) => {
              const bsModal = bootstrap.Modal.getInstance(modal)
              if (bsModal) {
                bsModal.hide()
              }
            })
            // Update cart count if it's returned in the response
            if (data.cart_count !== undefined) {
              updateCartBadge(data.cart_count);
            }
            window.location.reload()
          }
        })
    })
  })
})


