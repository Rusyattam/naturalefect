class ScrollTo {
   constructor(obj) {
      this.$el = document.querySelectorAll(`a:not(.${obj.block}), ${obj.addClass}`);
      this.target = obj.target;
      this.type = obj.type;
      this._cta = document.querySelector(this.target);
      this.scroll();
   }

   handleEvent(event) {
      event.preventDefault();
      this._cta.scrollIntoView({ block: `${this.type ? this.type : "center"}`, behavior: "smooth" });
   }

   scroll() {
      const html = document.querySelector("html");
      const body = document.querySelector("body");
      html.style.scrollBehavior = "smooth";
      body.style.scrollBehavior = "smooth";
      this.$el.forEach((element) => {
         element.setAttribute("href", this.target);
         element.addEventListener("click", this);
      });
   }
}
