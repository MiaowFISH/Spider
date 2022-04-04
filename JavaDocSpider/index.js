const jsdom = require('jsdom')
const { JSDOM } = jsdom
const { log } = require('console')

const request = require('request')
let URL = 'https://www.matools.com/file/manual/jdk_api_1.8_google/java/nio/file/Files.html'
async function getHTML(url) {
  return new Promise((resolve, reject) => {
    request(url, (err, res, body) => {
      if (err) {
        reject(err)
      } else {
        resolve(body)
      }
    })
  })
}

function getHead(table) {
  switch (table.querySelector('th').textContent) {
    case '接口':
      return 'interface'
    case '类':
      return 'class'
    case 'Enum':
      return 'enum'
    default:
      break
  }
}
function myTrim(x) {
  return x.replace(/^\s+|\s+$/gm, '')
}
function replaceType(text) {
  return text
    .replace('int', 'number')
    .replace('long', 'number')
    .replace('short', 'number')
    .replace('float', 'number')
    .replace('double', 'number')
    .replace('boolean', 'boolean')
    .replace('char', 'string')
    .replace('...', '[]')
}
function handel(table) {
  let list = table.querySelectorAll('tbody')[1].querySelectorAll('tr')
  let head = getHead(table)
  list.forEach((item) => {
    let name = item.querySelector('td.colFirst').textContent
    let desc = item.querySelector('td.colLast').textContent
    desc = desc.replace(/\s+/g, ' ').replace(/\n/g, ' ').replace('。', '').trimEnd()
    log(`/** ${desc} */`)
    log(`${head} ${name} {}`)
  })
}
function handelMethod(table) {
  let list = table.querySelector('table > tbody').querySelectorAll('tr[id]')
  list.forEach((item) => {
    let modifier = item.querySelector('td.colFirst').textContent.split(' ')[0]
    let type = item.querySelector('td.colFirst').textContent.replace(modifier, '').trim()
    let method = item.querySelector('td.colLast').querySelector('code').textContent
    methodName = method.split('(')[0]

    let params = method.split('(')[1].split(')')[0].split(',')
    params = params.map((item) => {
      let param = myTrim(item).split(/\s/)
      let name = param[1].replace('in', 'input')
      let type = param[0]
      return `${name}: ${replaceType(type)}`
    })
    let desc = item.querySelector('td.colLast').querySelector('div.block').textContent
    desc = desc.replace(/\s+/g, ' ').replace(/\n/g, ' ').replace('。', '').trimEnd()
    log(`/** ${myTrim(desc)} */`)
    log(`${modifier} ${methodName}(${params.join(', ')}): ${replaceType(type)}`)
    //log(`${name}() {}`)
  })
}

getHTML(URL).then((html) => {
  const dom = new JSDOM(html)
  let interfaceTable = dom.window.document.querySelectorAll('table')[0]
  let classTable = dom.window.document.querySelectorAll('table')[1]
  let enumTable = dom.window.document.querySelectorAll('table')[2]

  handelMethod(dom.window.document)
})
