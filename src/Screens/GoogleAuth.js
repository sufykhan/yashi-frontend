import React,{useEffect,useState} from 'react'

import GoogleLogin from 'react-google-login';
import { useHistory } from 'react-router';




function Signin() {

    const history=useHistory();
    const [name,setName]=useState('');
    const responseGoogle=async(response)=>{
        console.log(response);
        const token=await response.profileObj.name;
        setName(token);
    }
    return (
        <div >
            <div>
                <div>
                  <div>
                    <h3>INDIAN INSTITUTE OF TECHNOLOGY JAMMU</h3>
                    <p>Login with One Step </p>
                    <button onClick={()=>history.push("/courses")} style={{cursor:"pointer"}}><span>Signin With Google</span></button>
                    {name!=''?<h1>Welcome {name}</h1>:
                    <GoogleLogin
                        clientId='3628049175-305lfr60td466e2kjd0fjg0pm9ergu7a.apps.googleusercontent.com'
                        buttonText="LOGIN WITH GOOGLE"
                        onSuccess={responseGoogle}
                        onFailure={responseGoogle}
                    />
                    }
                  </div>
                </div>

            </div>
            
        </div>
    )
}

export default Signin









// const dispatch = useDispatch();
// const {userInfo,error,loading}=useSelector(state=>state.userBasicDetail)

// //console.log(userInfo);

// const history=useHistory();
// const [token,setToken]=useState("")
// // const [useremail,setUseremail] = useState("")
// const responseGoogle = async(response) => {
//     // let googleResponse  = await googleLogin(response.accessToken)
//     // console.log(googleResponse);
//     // console.log(response);
//     localStorage.setItem('userAvatar', response.profileObj.imageUrl)
//     // console.log(response.profileObj.imageUrl)
//     setToken(response)
//   }
//   useEffect(() => {
//     if(userInfo){
//       //  history.push("/courses")
//     }
   
// }, [history,userInfo])

// useEffect(() => {
   
//     if(token!==""){
//     // const headers = {
//     //     'Content-Type': 'application/json',
//     // }
    
//     const resi=async()=>{
//         try{
       
//         if((token.profileObj.email).split('@')[1]==="iitjammu.ac.in"){
//             // const What=await axios.post("http://localhost:8000/social-login/google/",{access_token:token.accessToken},headers);
//             // localStorage.setItem('userEmail', What.data.user.email);
//             // localStorage.setItem('accessGrant',What.data.access_token);
//             dispatch(login(token.accessToken));
           
//         } 
//         else{
//             console.log("Not from organisation")
//             // return {"Error":"Not from organisation"}
//         }
//         }
//         catch(error){
//             console.log(error);
//         }
//         history.push("/");
//     }
//     resi();
// }
// }, [token,dispatch,history])
// // const googleLogin = async (accesstoken) => {
// //     let res = await axios.post(
// //       "http://localhost:8000/rest-auth/google/",
// //       {
// //         access_token: accesstoken,
// //       }
// //     );
// //     console.log(res);
// //     return await res.status;
// //   };
// const { CLIENT_ID_GOOGLE } = process.env;