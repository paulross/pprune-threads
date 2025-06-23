
=========================
Remixes of prune threads.
=========================

--------------------------------------------
Air India Flight 171 at Ahmedabad 2025-06-12
--------------------------------------------

https://en.wikipedia.org/wiki/Air_India_Flight_171

https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html

Pulling Down the Thread(s)
--------------------------

```shell
$ cd threads/AI171-1
$ curl https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html -o "666472-plane-crash-near-ahmedabad.html"
$ grep 'Last Page' 666472-plane-crash-near-ahmedabad.html
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

Then:

```shell
$ cd threads/AI171-2
$ curl https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html -o "666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html"
$ grep 'Last Page' 666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html
```

This gives:

```shell
	<li><a id="mb_pagelast" class="button primary hollow" href="https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html?ispreloading=1" title="Last Page - Results 1,061 to 1,074 of 1,074">Last <i class="fas fa-angle-double-right"></i></a></li>```

So the last page is ``https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html``

And all the rest:

```shell
$ time curl https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-[2-56].html -o "666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-#1.html"
...
real	0m35.544s
user	0m0.176s
sys	0m0.356s
```






