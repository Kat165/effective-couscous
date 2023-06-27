(() => {
const $ = selector => document.querySelector(selector)

const box1El = $('.box1')
const box2El = $('.box2')
const box3El = $('.box3')
const boxEls = [box1El, box2El, box3El]

const btnPropagationEl = $('.but-startpropagation')
const btnPropagationElStop = $('.but-stoppropagation')
const btnResetEl = $('.but-reset')
const messagesBoxEl = $('.message-list-added')
const counterEl = $('.point')

const messageClassStr = 'message'

let counter = 0
let isPropagationEnabled = false
const eventHandlers = []

const handleBoxClick = targetEl => {
    const color   = targetEl.getAttribute('data-color')
    const points  = parseInt(targetEl.getAttribute('data-points'))
    const message = `Nacisnąłeś ${color} box!`
    const threshold = parseInt(targetEl.getAttribute('data-threshold')) || Infinity

    return e => {
        counter += points

        if (!isPropagationEnabled) e.stopPropagation()

        setTimeout(() => {
            if (counter >= threshold) disableBox(targetEl)
        }, 0)

        displayMessage(`[${counter}]`.padEnd(5) + message)
        updateCounter()
    }
}

const addEventHandlers = boxElsArr => {
    boxElsArr.forEach(boxEl => eventHandlers.push(['click', handleBoxClick(boxEl)]))
}
addEventHandlers(boxEls)

const togglePropagation = () => {
    isPropagationEnabled = !isPropagationEnabled
    btnPropagationEl.innerText = `${isPropagationEnabled ? 'Stop' : 'Start'} propagation`
}

const disableBox = targetEl => {
    const i = boxEls.indexOf(targetEl)
    if (i >= 0) targetEl.removeEventListener(...eventHandlers[i])
    targetEl.classList.add('disabled')
}

const displayMessage = message => {
    const messageEl = document.createElement('li')
    messageEl.classList.add(messageClassStr)
    messageEl.innerHTML = message
    messagesBoxEl.appendChild(messageEl)

    messagesBoxEl.parentElement.scrollTo({
        top: messageEl.offsetTop ,
        behavior: 'smooth'
    })
}

const updateCounter = () => {
    counterEl.innerText = counter
}

const setupEventListeners = () => {
    boxEls.forEach((boxEl, i) => boxEl.addEventListener(...eventHandlers[i]))
}

const handleReset = () => {
    counter = 0
    messagesBoxEl.innerHTML = ''
    boxEls.forEach(boxEl => boxEl.classList.remove('disabled'))
    setupEventListeners()
    updateCounter()

    messagesBoxEl.parentElement.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
}

// Setup event listeners
setupEventListeners()
btnPropagationEl.addEventListener('click', togglePropagation)
btnResetEl.addEventListener('click', handleReset)
})()
