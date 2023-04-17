const commonUrl = 'http://127.0.0.1:5004'
localStorage.setItem("access_token","test")

// function parseJSON(response){
//     return response.json()
// }
function assembleUrl(route, text){
    return commonUrl+'/'+route+'?text='+text;
}

function checkStatus(response){
    if(response.status >= 200 && response.status < 500){
        return response
    }
    const error = new Error(response.statusText)
    error.response = response
    throw error
}

export default  function request(options = {}){
    // const Authorization = localStorage.getItem('access_token')
    const {data, route, text} = options
    options = {...options}
    options.mode = 'cors'
    if(data){
        delete options.data
        options.body = JSON.stringify({
            data
        })
    }
    // options.headers={
    //     // 'Authorization':Authorization,
    //     'Content-Type':'application/json'
    // }
    return fetch(assembleUrl(route, text),options,{credentials: 'include'})
        .then(checkStatus)
        // .then(parseJSON)
        .catch(err=>({err}))
}