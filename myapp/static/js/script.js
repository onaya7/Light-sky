let popup = document .getElementById("popup");

function openCard(){
    popup.classList.add("open-popup")
}

function closeCard(){
    popup.classList.remove("open-popup") ;
}


$(document).ready(function(){

    $('form').on ('submit', function(event){
            $.ajax({
                data : {
                    name : $('#nameInput').val(),
                },
                type : 'POST',
                url: '/process_data'
            })

            .done(function(data){
                    console.log(data)
                    console.log(data.name)
                    // console.log(data.name.date)
                    // console.log(data.name.description)
                    // console.log(data.name.humidity)
                   
                    if (data.name){
                            $( '#location').html(`<p><span><i class="fa-solid fa-location-dot"></i></span>${data.name.city}</p>`);

                            $('#date').html(`<p><span><i class="fa-solid fa-calendar-days"></i></span>
                            ${data.name.date}</p>`);


                            $('#icon-img').html(
                                `  <img src="http://openweathermap.org/img/w/${data.name.icon}.png" alt="Image">
                                <p>${data.name.description}</p>`
                            );

                            $('#temperature').html(
                                `   <p><span><i class="fa-brands fa-pagelines"></i></span> Temperature</p>
                                <p>${data.name.temperature}ºC</p>`
                            );

                            $('#humidity').html(
                                `   <p><span><i class="fa-solid fa-droplet"></i></span> Humidity</p>
                                <p>${data.name.humidity}%</p>`
                            );

                            $('#wind').html(
                                `   <p><span><i class="fa-solid fa-wind"></i></span> Wind</p>
                                <p>${data.name.wind}km/h</p>`
                            );

                            $('#time').html(
                                `   <p><span><i class="fa-solid fa-clock"></i></span> Time</p>
                                <p>${data.name.time}</p>`
                            );
                            
                    }
                       

                    if(data.error){
                        $( '#location').html(`<p><span><i class="fa-solid fa-location-dot"></i></span>not found</p>`);

                            $('#date').html(`<p><span><i class="fa-solid fa-calendar-days"></i></span>
                            not found</p>`);


                            $('#icon-img').html(
                                `<span>${data.error}</span> 
                                <i class="fa-solid fa-face-frown"></i>
                                `
                                
                            );

                            $('#temperature').html(
                                `   <p><span><i class="fa-brands fa-pagelines"></i></span> Temperature</p>
                                <p>not found</p>`
                            );

                            $('#humidity').html(
                                `   <p><span><i class="fa-solid fa-droplet"></i></span> Humidity</p>
                                <p>not found</p>`
                            );

                            $('#wind').html(
                                `   <p><span><i class="fa-solid fa-wind"></i></span> Wind</p>
                                <p>not found</p>`
                            );

                            $('#time').html(
                                `   <p><span><i class="fa-solid fa-clock"></i></span> Time</p>
                                <p>not found</p>`
                            );
                            
                    }

            });
            event.preventDefault();
    });
});