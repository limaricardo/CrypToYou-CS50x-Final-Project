function calculator(){
    var priceChange1 = document.getElementById("priceChange1").value; 
    var priceChange2 = document.getElementById("priceChange2").value; 
    var poolWeight1 = document.getElementById("poolWeight1").value; 
    var poolWeight2 = document.getElementById("poolWeight2").value; 
    var impLoss = document.getElementById("impermanentLoss");


    if (priceChange1 == null || priceChange2 == null || poolWeight1 == null || poolWeight2 == null) {
        return 1;
    }

    if (priceChange1 == 0 && priceChange2 == 0 && poolWeight1 == 0 && poolWeight2 == 0 || (poolWeight1 == 0 && poolWeight2 == 0)) {
        return 1
    }


    asset1 = (priceChange1 / 100) + 1  
    asset2 = (priceChange2 / 100) + 1  
    valueOfPool = (asset1 ** (poolWeight1 / 100)) * (asset2 ** (poolWeight2 / 100)) 
    valueIfHeld = ((asset1 * poolWeight1)/100) + ((asset2 * poolWeight2)/ 100)
    impermanentLoss = (((valueOfPool / valueIfHeld) - 1) * (-100)).toFixed(2)

    impLoss.innerHTML = impermanentLoss
}