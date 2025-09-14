const maxPriceField = document.getElementById("max_price_input");
const minPriceField = document.getElementById("min_price_input");

const lowerRange = document.getElementById("lower_range");
const upperRange = document.getElementById("upper_range");

const valueLover = document.getElementById("range_value_lower");
const valueUpper = document.getElementById("range_value_upper");

lowerRange.value = lowerRange.max*0.2;
upperRange.value = upperRange.max*0.8;

maxPriceField.value = upperRange.value;
minPriceField.value = lowerRange.value;

valueLover.textContent = "$" + lowerRange.value;
valueUpper.textContent = "$" + upperRange.value;

function updatePriceInputsValues(rangeValue, range, priceField){
    rangeValue.textContent = "$" + range.value;
    priceField.value = range.value;
}

function updatePriceRangesValues(rangeValue, range, priceField){
    rangeValue.textContent = "$" + priceField.value;
    range.value = priceField.value;
}

lowerRange.addEventListener('input', function(){
    updatePriceInputsValues(valueLover, lowerRange, minPriceField);
})

upperRange.addEventListener('input', function(){
    updatePriceInputsValues(valueUpper, upperRange, maxPriceField);
})

minPriceField.addEventListener('input', function(){
    updatePriceRangesValues(valueLover, lowerRange, minPriceField);
})

maxPriceField.addEventListener('input', function(){
    updatePriceRangesValues(valueUpper, upperRange, maxPriceField);
})