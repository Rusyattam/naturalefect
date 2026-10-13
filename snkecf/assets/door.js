class GenerateCta {
   constructor(selector) {
      this.$el = document.querySelector(selector);
      this.options = {};
      this.doorItemElements = this.$el.querySelectorAll(".door__item");
      this.discountElements = [this.$el.querySelector(".door__item-discount[data-discount='0']"), this.$el.querySelector(".door__item-discount[data-discount='1']"), this.$el.querySelector(".door__item-discount[data-discount='2']")];
   }

   handleEvent = (event) => {
      if (event.currentTarget.classList.contains("door__item")) {
         const door = this.$el.querySelector(".door");

         event.currentTarget.classList.add("open");
         this.discount(event);

         this.doorItemElements.forEach((door) => {
            door.removeEventListener("click", this);
            setTimeout(() => {
               door.classList.add("open");
            }, 1000);
         });

         setTimeout(() => {
            door.classList.add("hidden");
            this.spin(this._options.scroll.target, this._options.scroll.type);
            this.order();
         }, 2500);

         setTimeout(() => {
            door.classList.add("none");
         }, 3800);
      }
   };

   door(options) {
      const orederImg = this.$el.querySelector(".order__img");
      const productNameElements = this.$el.querySelectorAll(".cta__name-product");

      this._options = options;

      this.doorItemElements.forEach((door) => {
         door.addEventListener("click", this);
      });

      orederImg.setAttribute("src", options.img);
      productNameElements.forEach((element) => {
         element.innerText = options.product;
      });
   }

   discount(event) {
      const discount = this.$el.querySelector(".price_land_discount").textContent;
      const replaceDiscount = discount === "50" ? "35" : "50";

      if (event.currentTarget.dataset.index === "0") {
         this.discountElements[0].textContent = `${discount}%`;
         this.discountElements[1].textContent = `${replaceDiscount}%`;
         this.discountElements[2].textContent = "25%";
      }
      if (event.currentTarget.dataset.index === "1") {
         this.discountElements[0].textContent = `${replaceDiscount}%`;
         this.discountElements[1].textContent = `${discount}%`;
         this.discountElements[2].textContent = "25%";
      }
      if (event.currentTarget.dataset.index === "2") {
         this.discountElements[0].textContent = "25%";
         this.discountElements[1].textContent = `${replaceDiscount}%`;
         this.discountElements[2].textContent = `${discount}%`;
      }
   }

   spin = (selector, type) => {
      const spin = this.$el.querySelector(".spin");
      const scroll = this.$el.querySelector(selector);
      const btnClose = spin.querySelector(".spin__btn");

      spin.classList.add("active");
      btnClose.addEventListener("click", () => {
         spin.classList.remove("active");
         scroll.scrollIntoView({ block: type, behavior: "smooth" });
         this.timer();
      });
   };

   order = () => {
      const order = this.$el.querySelector(".order");
      order.classList.add("active");

      // Вызов метода валидации инпутов
      this.validateInputs();
   };

   timer = () => {
      const minuteElement = this.$el.querySelector("#orderMinute");
      const secondElement = this.$el.querySelector("#orderSecond");
      let timer = 60 * (10 - 0.01);

      const updateTimer = () => {
         const minutes = parseInt(timer / 60, 10);
         const seconds = parseInt(timer % 60, 10);

         minuteElement.innerHTML = minutes < 10 ? "0" + minutes : minutes;
         secondElement.innerHTML = seconds < 10 ? "0" + seconds : seconds;

         if (--timer < 0) {
            timer = 0;
            clearInterval(id);
         }
      };

      const id = setInterval(updateTimer, 1000);
   };

   validateInputs = () => {
      const nameInput = this.$el.querySelector(".order__input[type='text']");
      const phoneInput = this.$el.querySelector(".order__input[type='tel']");

      const validateInput = (input, regex) => {
         input.value = input.value
            .split("")
            .filter((char) => regex.test(char))
            .join("");
      };

      // Валидация для имени (только буквы и пробелы)
      if (nameInput) {
         nameInput.addEventListener("input", () => {
            validateInput(nameInput, /^[A-Za-zА-Яа-яЁё\s]*$/);
         });
      }

      // Валидация для телефона (только цифры)
      if (phoneInput) {
         phoneInput.addEventListener("input", () => {
            validateInput(phoneInput, /^\+?\d*$/);
         });
      }
   };
}
