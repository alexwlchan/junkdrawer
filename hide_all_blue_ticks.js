function dimTheBlueTicks() {
    var articles = document.getElementsByTagName("article");

    // Basic gist: on the Twitter timeline, individual tweets are <article>s,
    // and quoted tweets are <div>'s with role="blockquote".
    //
    // For each tweet:
    //
    //  - How many verified users are in the overall tweet?
    //  - How many verified users are in the quoted tweet (if any)?
    //
    // If the only verified user is in the quoted tweet, just dim that; otherwise
    // dim the whole tweet.
    for (var i = 0; i < articles.length; i++) {
        var verifiedCount = 0;
        var svgs = articles[i].getElementsByTagName("svg");
        for (var j = 0; j < svgs.length; j++) {
            if (svgs[j].ariaLabel == "Verified account") {
                verifiedCount += 1;
    		}
    	}

        var quotedVerifiedCount = 0;

        if (articles[i].querySelectorAll('[role="blockquote"]').length > 0) {
            var blockquote = articles[i].querySelectorAll('[role="blockquote"]')[0];
            var blockquoteSvgs = blockquote.getElementsByTagName("svg");
            for (var k = 0; k < blockquoteSvgs.length; k++) {
                if (blockquoteSvgs[k].ariaLabel == "Verified account") {
                    quotedVerifiedCount += 1;
        		}
        	}
        }

        if (quotedVerifiedCount >= 1 && verifiedCount == 1) {
            // Dim the inner element rather than the whole tweet, so you still
            // get a visible border around the whole quoted tweet.
            blockquote.getElementsByTagName("div")[0].style.opacity = 0.15;
        } else if (verifiedCount >= 1) {
            articles[i].style.opacity = 0.15;
        }
    }

    // Run repeatedly -- the timeline has infinite scroll, so we need to dim
    // newly-loaded tweets as necessary.
    setTimeout(function() { dimTheBlueTicks() }, 100);
}

dimTheBlueTicks();
