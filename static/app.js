$('form input[type="file"]').change(event => {
    let arquivos = event.target.files;
    if (arquivos.length === 0) {
      console.log('sem imagem pra mostrar')
    } else {
        let tiposPermitidos = ['image/jpeg', 'image/png', 'image/gif'];
        console.log(arquivos)
        if(tiposPermitidos.includes(arquivos[0].type)) {
          $('img').remove();
          let imagem = $('<img class="img-fluid">');
          imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
          $('figure').prepend(imagem);
        } else {
          alert('Formato não suportado')
        }
    }
  });