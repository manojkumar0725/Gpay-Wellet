const userfrm =document.getElementById("logfrm");
userfrm.addEventListener("submit",(e)=>{
  e.preventDefault();
  let usrid = "summa123";
  let usrpwd = "summa@123";
  let usrnum = "1234567890";
  const userid =document.getElementById("userId").value;
  const userpwd =document.getElementById("userpassword").value;
  const usernum =document.getElementById("usernumber").value;
  if(userid == "" && userid == "" && usernum == ""){
    alert("Enter the All field!");
    return;
  }
   if(userid == ""){
    alert("Enter The UserId");
    return;
  }else if(userid !== usrid){
    alert("Enter The Correct User Id");
    return;
  }
   if(userpwd == ""){
    alert("Fill The UserPassword");
    return;
  }else if(userpwd !== usrpwd){
    alert("Enter The Correct User Password");
    return;
  }
   if(usernum == ""){
    alert("Fill The Number");
    return;
  }else if(usernum !== usrnum){
    alert("Enter The Correct Number");
    return;
  }
  alert("Successfuly Login✅");
  window.location.href = "Homepage.html";
});