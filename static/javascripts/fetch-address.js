

// async function getAddressFromPlacesAPI(uprn, key){

//     try{
//         const response = await fetch(`https://api.os.uk/search/places/v1/uprn?uprn=${uprn}&key=${key}`)    
//         const data = await response.json()
//         const address = data['results'][0]['DPA']['ADDRESS']
//         return address
//     }
//     catch{
        
//     }
    

// }
// async function setAddress(id, uprn, key){
  
//     const element = document.getElementById(id)
//     address = await getAddressFromPlacesAPI(uprn, key)
//     element.innerHTML = await address

// }