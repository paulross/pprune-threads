# prune-threads
Remixes of prune threads.


## Air India Flight 171 at Ahmedabad 2025-06-12

https://en.wikipedia.org/wiki/Air_India_Flight_171

https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html

### Pulling Down the Thread

```shell
$ cd threads/AI171
$ curl https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html -o "666472-plane-crash-near-ahmedabad-1.html"
$ grep 'Last Page' 666472-plane-crash-near-ahmedabad-1.html
```

This gives:

```shell
	<li><a id="mb_pagelast" class="button primary hollow" href="https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-87.html?ispreloading=1" title="Last Page - Results 1,721 to 1,729 of 1,729">Last <i class="fas fa-angle-double-right"></i></a></li>
```

So the last page is ``666472-plane-crash-near-ahmedabad-87.html``

And all the rest:

```shell
$ time curl https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-[2-87].html -o "666472-plane-crash-near-ahmedabad-#1.html"
...
real	0m35.544s
user	0m0.176s
sys	0m0.356s
```






