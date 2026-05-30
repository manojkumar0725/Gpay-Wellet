 const register = document.getElementById("reg");
    register.addEventListener("submit", (e)=>{
      e.preventDefault();
      const names = document.getElementById("name").value;
      const userid = document.getElementById("userid").value;
      const upass = document.getElementById("upass").value;
      const email = document.getElementById("emai").value;
      const epass = document.getElementById("epass").value;
      const mobile = document.getElementById("mobile").value;
      if(names =="" && upass =="" && email =="" && epass =="" && mobile ==""){
        alert("all fill form");
        return;
      }
      if (mobile != 10) {
        
      }
      if(names ==""){
        alert("Enter The Name");
        return;
      }
      if(userid ==""){
        alert("Enter The UserId");
        return;
      }
      if(upass ==""){
        alert("Enter The Password");
        return;
      }
      if(mobile ==""){
        alert("Enter The Mobile Number");
        return;
      }
      if(email ==""){
        alert("Enter The Email Id");
        return;
      }
      if(epass ==""){
        alert("Enter The Email Password");
        return;
      }
      
      alert("succsess fully ");
      window.location.href="Loginpage.html";
    });