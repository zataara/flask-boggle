class BoggleGame {
/* Create a new Boggle Game*/

    constructor(boardId, secs = 60){
        this.secs = secs; //Game length
        this.score = 0;
        this.words = new Set();
        this.boardId = $('#' + boardId);
        this.timer = setInterval(this.tick.bind(this), 1000);
        this.showTimer();

        $('.add-word', this.board).on('submit', this.handleSubmit.bind(this))
    }

    showWord(word){
        //take valid submitted word and append to DOM as list element
        $('.words', this.board).append($('<li>', {text: word}));
    }

    showScore(){
        $('.score', this.board).text(this.score)
    }

    showMessage(msg, cls) {
        $(".msg", this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }
    
    async handleSubmit(evt){
        evt.preventDefault();
        const $word = $("#word", this.board);
        
        let word = $word.val();
            //grab value of form input
        
        if(!word){
            //check to make sure text has been entered
            return
        }
        
        if(this.words.has(word)){
            //check words already entered
            this.showMessage('Already found word', 'err')
            return
        }
        
        const res = await axios.get("/check-word", { params: { word: word }});
        if (res.data.result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (res.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }
    }

    showTimer(){
        $('.timer', this.board).text(this.secs);
    }


    async tick(){
        //handle 1 second time change
        this.secs -= 1;
        this.showTimer();
        if (this.secs <= 10){
            $('.timer', this.board).addClass('final-seconds')
        }
        if (this.secs === 0){
            clearInterval(this.timer)
            await this.scoreGame();
        }
    }

    async scoreGame(){
        $('.add-word', this.board).hide();
        const res = await axios.post('/post_score', {score: this.score});
        if (res.data.brokeRecord){
            this.showMessage(`New Record: ${this.score}`, 'ok')
        } else {
            this.showMessage(`Highscore: ${this.score}`, 'ok')
        }

    }








}