


function generateCupcakeHTML(cupcake){
    return `<div><li><p>Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}</p>
    <img src="${cupcake.image}" alt="${cupcake.flavor}" height="250"></img>
    <button class="delete-cupcake" id="${cupcake.id}">X</button> </li></div>`
}

async function showInitalCupcakes(){
    const response = await axios.get("/api/cupcakes")
    for (let cupcake of response.data.cupcakes){
        let newCupcake = generateCupcakeHTML(cupcake);
        $("#cupcakes-list").append(newCupcake);
    }
}

$("#new-cupcake-form").on("submit", async function(evt){
    evt.preventDefault();
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const response = await axios.post("/api/cupcakes", {flavor, rating, size, image});

    let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger('reset');
})

showInitalCupcakes();

$("#cupcakes-list").on("click", ".delete-cupcake", async function (evt){
    let $cupcake = $(evt.target).closest("div");
    let id = evt.target.id;
    await axios.delete(`/api/cupcakes/${id}`)
    $cupcake.remove();
})
       