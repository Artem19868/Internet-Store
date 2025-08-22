const lowerRange = document.getElementById("lower_range");
const upperRange = document.getElementById("upper_range");

const valueLover = document.getElementById("range_value_lower");
const valueUpper = document.getElementById("range_value_upper");

lowerRange.value = lowerRange.max*0.2;
upperRange.value = upperRange.max*0.8;

valueLover.textContent = "$" + lowerRange.value;
valueUpper.textContent = "$" + upperRange.value;

lowerRange.addEventListener('input', function(){
    valueLover.textContent = "$" + lowerRange.value;
})

upperRange.addEventListener('input', function(){
    valueUpper.textContent = "$" + upperRange.value;
})