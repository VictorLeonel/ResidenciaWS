const puppeteer = require('puppeteer');
const mongoose = require('mongoose');
const fs = require('fs-extra');
const Titulos = require('./models/Titulos');
// const conexion = require('./conexion');



//********************************************* Conexiona a MongoDB ********************************************
const user='admin1';
const password='passwordresidencia';
const dbname = 'proyectoRWS';
const uri = `mongodb+srv://${user}:${password}@cluster0.pwuxu.mongodb.net/${dbname}?retryWrites=true&w=majority`;

mongoose.connect(uri, {
    useNewUrlParser: true, useUnifiedTopology: true
})
    .then(() => console.log('Base de datos conectada'))
    .catch(e => console.log(e))
// *********************************************************************************************************



// *************************************** URL y Seccion de Noticias ***************************************
// URL de Paginas de Noticias
const urlElpais = "https://elpais.com/mexico/";  
const urlMilenio = "https://www.milenio.com/ultima-hora";
const urlUniversal = "https://www.eluniversal.com.mx/";


// Ruta de seccion en donde estan las Noticias
const NoticiaElpais = '#fusion-app > main > div.z.z-hi > section > div.b-d_b.b_op._g._g-md.b_op-1-2 > article';
const NoticiaMilenio = "body > div.body-content > div > div > div > div > div.list-news-container > div > div:nth-child(1)";
const NoticiaUniversal = "#contenedor > div.contenido-principal > div > div > div:nth-child(2) > div.gl-Grid_9 > div > div.notas-principales > div.nota-principal";
// ************************************************************************************************************



// ******************************************** Scrapin de Paginas *********************************************
// Scrapina pagina El Milenio
async function ElPais() {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();      
        await page.goto(urlElpais,{waitUntil: 'networkidle2', timeout: 0});
        await page.click('#didomi-notice-agree-button');//Darle click en el boton de cookie                      
        await page.waitForSelector(NoticiaElpais); 
        const noticia = await page.$(NoticiaElpais);
        await noticia.screenshot({
            path: 'capturas/NoticiaElPais.png'
        });
        /*  // Buscar el titulo y resumen de la noticia principal y guardarlo*/ 
        const paginaElpais = "El Pais";
        const tituloElpais = await page.$eval("#fusion-app > main > div.z.z-hi > section > div.b-d_b.b_op._g._g-md.b_op-1-2 > article > header", el => el.innerText.trim());
        const resumenElpais = await page.$eval("#fusion-app > main > div.z.z-hi > section > div.b-d_b.b_op._g._g-md.b_op-1-2 > article > p", el => el.innerText.trim());
        await console.log("\nPagina: "+paginaElpais+"\nTitulo: "+tituloElpais+"\nResumen: "+resumenElpais+"\n");
    
        //  ************************************ Guardando los encabezados ************************************
        const encabezado = new Titulos({pagina: paginaElpais, titulo: tituloElpais, resumen: resumenElpais});
        encabezado.save(function (err) {
            if (err) {
                console.log(err);
            } else {
                console.log('Noticia El Pais Guardado');
            }
        }); 
        await page.close();                        
        await browser.close();                    
    } catch (error) {
        console.log("La Pagina El Pais no Carga")
    }
};
ElPais();



// Scrapin a pagina El Milenio
async function Milenio() {
    try {
        const browser = await puppeteer.launch();  
        const page = await browser.newPage();      
        await page.goto(urlMilenio,{waitUntil: 'networkidle2', timeout: 0});                  
        await page.click('#cookie-disclaimer > div > div > button');//Darle click en el boton de cookie                      
        await page.waitForSelector(NoticiaMilenio); 
        const noticia = await page.$(NoticiaMilenio);
        await noticia.screenshot({
            path: 'capturas/NoticiaMilenio.png'
        });
        /*  // Buscar el titulo y resumen de la noticia principal y guardarlo*/ 
        const paginaMilenio = "Milenio";
         const tituloMilenio = await page.$eval("body > div.body-content > div > div > div > div > div.list-news-container > div > div:nth-child(1) > div > div.title-container > div.title", el => el.innerText.trim());
         const resumenMilenio = await page.$eval("body > div.body-content > div > div > div > div > div.list-news-container > div > div:nth-child(1) > div > div.title-container > div.summary", el => el.innerText.trim());
         await console.log("\nPagina: "+paginaMilenio+"\nTitulo: "+tituloMilenio+"\nResumen: "+resumenMilenio+"\n");
            
         //  ************************************ Guardando los encabezados ************************************
         const encabezado = new Titulos({pagina: paginaMilenio, titulo: tituloMilenio, resumen: resumenMilenio});
         encabezado.save(function (err) {
             if (err) {
                 console.log(err);
             } else {
                 console.log('Noticia Milenio Guardado');
             }
         }); 
         await page.close();                        
         await browser.close();                    
    } catch (error) {
        console.log("La Pagina El Milenio no Carga")
    }
};
Milenio();



// Scraping a pagina Universal
async function Universal() {
    try {
        const browser = await puppeteer.launch();  
        const page = await browser.newPage();      
        await page.goto(urlUniversal,{waitUntil: 'networkidle2', timeout: 0});                      
        await page.click('#popup-buttons');//Darle click en el boton de cookie                      
        await page.waitForSelector(NoticiaUniversal); 
        const captura = await page.$(NoticiaUniversal);
        await captura.screenshot({
            path: 'capturas/NoticiaUniversal.png'
        });
        // Buscar el titulo y resumen de la noticia principal
        const paginaUniversal = "El Universal";
        const tituloUniversal = await page.$eval(".nota-principal > .titulo > a", el => el.innerText.trim());
        const resumenUniversal = await page.$eval(".nota-principal > .resumen", el => el.innerText.trim());
        await console.log("\nPagina: "+paginaUniversal+"\nTitulo: "+tituloUniversal+"\nResumen: "+resumenUniversal+"\n");

        //  ************************************ Guardando los encabezados ************************************
        const encabezado = new Titulos({pagina: paginaUniversal, titulo: tituloUniversal, resumen: resumenUniversal});
        encabezado.save(function (err) {
            if (err) {
                console.log(err);
            } else {
                console.log('Noticia Universal Guardado');
            }
        });
        await page.close();                        
        await browser.close();
        
    } catch (error) {
        console.log("La Pagina Universal no Carga")
    }
};
Universal();

console.log("\n Fin del scraping \n")