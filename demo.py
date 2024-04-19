from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
This script is just to show that the selected summarization technology works. Next step is to try with longer texts.
Running it the first time takes awhile.
Swap in any of the four texts provided in inputs to see the different summaries.
"""

# From the introduction to "The Ethics of Aristotle"
text1 = """
The _Ethics_ of Aristotle is one half of a single treatise of which his
_Politics_ is the other half. Both deal with one and the same subject.
This subject is what Aristotle calls in one place the “philosophy of
human affairs;” but more frequently Political or Social Science. In the
two works taken together we have their author’s whole theory of human
conduct or practical activity, that is, of all human activity which is
not directed merely to knowledge or truth. The two parts of this
treatise are mutually complementary, but in a literary sense each is
independent and self-contained. The proem to the _Ethics_ is an
introduction to the whole subject, not merely to the first part; the
last chapter of the _Ethics_ points forward to the _Politics_, and
sketches for that part of the treatise the order of enquiry to be
pursued (an order which in the actual treatise is not adhered to).

The principle of distribution of the subject-matter between the two
works is far from obvious, and has been much debated. Not much can be
gathered from their titles, which in any case were not given to them by
their author. Nor do these titles suggest any very compact unity in the
works to which they are applied: the plural forms, which survive so
oddly in English (Ethic_s_, Politic_s_), were intended to indicate the
treatment within a single work of a _group_ of connected questions. The
unity of the first group arises from their centring round the topic of
character, that of the second from their connection with the existence
and life of the city or state. We have thus to regard the _Ethics_ as
dealing with one group of problems and the _Politics_ with a second,
both falling within the wide compass of Political Science. Each of
these groups falls into sub-groups which roughly correspond to the
several books in each work. The tendency to take up one by one the
various problems which had suggested themselves in the wide field
obscures both the unity of the subject-matter and its proper
articulation. But it is to be remembered that what is offered us is
avowedly rather an enquiry than an exposition of hard and fast
doctrine.
"""

# The opening of Milton's Paradise Lost
text2 = """
Of Man’s first disobedience, and the fruit
Of that forbidden tree whose mortal taste
Brought death into the World, and all our woe,
With loss of Eden, till one greater Man
Restore us, and regain the blissful seat,
Sing, Heavenly Muse, that, on the secret top
Of Oreb, or of Sinai, didst inspire
That shepherd who first taught the chosen seed
In the beginning how the heavens and earth
Rose out of Chaos: or, if Sion hill
Delight thee more, and Siloa’s brook that flowed
Fast by the oracle of God, I thence
Invoke thy aid to my adventurous song,
That with no middle flight intends to soar
Above th’ Aonian mount, while it pursues
Things unattempted yet in prose or rhyme.
And chiefly thou, O Spirit, that dost prefer
Before all temples th’ upright heart and pure,
Instruct me, for thou know’st; thou from the first
Wast present, and, with mighty wings outspread,
Dove-like sat’st brooding on the vast Abyss,
And mad’st it pregnant: what in me is dark
Illumine, what is low raise and support;
That, to the height of this great argument,
I may assert Eternal Providence,
And justify the ways of God to men.
"""

# The first few paragraphs of Augustine's Confessions
text3 = """
Great art Thou, O Lord, and greatly to be praised; great is Thy power,
and Thy wisdom infinite. And Thee would man praise; man, but a particle
of Thy creation; man, that bears about him his mortality, the witness of
his sin, the witness that Thou resistest the proud: yet would man praise
Thee; he, but a particle of Thy creation. Thou awakest us to delight in
Thy praise; for Thou madest us for Thyself, and our heart is restless,
until it repose in Thee. Grant me, Lord, to know and understand which is
first, to call on Thee or to praise Thee? and, again, to know Thee or
to call on Thee? for who can call on Thee, not knowing Thee? for he that
knoweth Thee not, may call on Thee as other than Thou art. Or, is it
rather, that we call on Thee that we may know Thee? but how shall they
call on Him in whom they have not believed? or how shall they believe
without a preacher? and they that seek the Lord shall praise Him: for
they that seek shall find Him, and they that find shall praise Him.
I will seek Thee, Lord, by calling on Thee; and will call on Thee,
believing in Thee; for to us hast Thou been preached. My faith, Lord,
shall call on Thee, which Thou hast given me, wherewith Thou hast
inspired me, through the Incarnation of Thy Son, through the ministry of
the Preacher.

And how shall I call upon my God, my God and Lord, since, when I call
for Him, I shall be calling Him to myself? and what room is there within
me, whither my God can come into me? whither can God come into me, God
who made heaven and earth? is there, indeed, O Lord my God, aught in me
that can contain Thee? do then heaven and earth, which Thou hast made,
and wherein Thou hast made me, contain Thee? or, because nothing which
exists could exist without Thee, doth therefore whatever exists contain
Thee? Since, then, I too exist, why do I seek that Thou shouldest enter
into me, who were not, wert Thou not in me? Why? because I am not gone
down in hell, and yet Thou art there also. For if I go down into hell,
Thou art there. I could not be then, O my God, could not be at all,
wert Thou not in me; or, rather, unless I were in Thee, of whom are all
things, by whom are all things, in whom are all things? Even so, Lord,
even so. Whither do I call Thee, since I am in Thee? or whence canst
Thou enter into me? for whither can I go beyond heaven and earth, that
thence my God should come into me, who hath said, I fill the heaven and
the earth.

Do the heaven and earth then contain Thee, since Thou fillest them? or
dost Thou fill them and yet overflow, since they do not contain Thee?
And whither, when the heaven and the earth are filled, pourest Thou
forth the remainder of Thyself? or hast Thou no need that aught contain
Thee, who containest all things, since what Thou fillest Thou fillest
by containing it? for the vessels which Thou fillest uphold Thee not,
since, though they were broken, Thou wert not poured out. And when Thou
art poured out on us, Thou art not cast down, but Thou upliftest us;
Thou art not dissipated, but Thou gatherest us. But Thou who fillest
all things, fillest Thou them with Thy whole self? or, since all things
cannot contain Thee wholly, do they contain part of Thee? and all at
once the same part? or each its own part, the greater more, the smaller
less? And is, then one part of Thee greater, another less? or, art Thou
wholly every where, while nothing contains Thee wholly?
"""

# The first few paragraphs of the Preface to the First Edition of Kant's Critique of Pure Reason
text4 = """
Human reason, in one sphere of its cognition, is called upon to
consider questions, which it cannot decline, as they are presented by
its own nature, but which it cannot answer, as they transcend every
faculty of the mind.

It falls into this difficulty without any fault of its own. It begins
with principles, which cannot be dispensed with in the field of
experience, and the truth and sufficiency of which are, at the same
time, insured by experience. With these principles it rises, in
obedience to the laws of its own nature, to ever higher and more remote
conditions. But it quickly discovers that, in this way, its labours
must remain ever incomplete, because new questions never cease to
present themselves; and thus it finds itself compelled to have recourse
to principles which transcend the region of experience, while they are
regarded by common sense without distrust. It thus falls into confusion
and contradictions, from which it conjectures the presence of latent
errors, which, however, it is unable to discover, because the
principles it employs, transcending the limits of experience, cannot be
tested by that criterion. The arena of these endless contests is called
_Metaphysic_.

Time was, when she was the _queen_ of all the sciences; and, if we take
the will for the deed, she certainly deserves, so far as regards the
high importance of her object-matter, this title of honour. Now, it is
the fashion of the time to heap contempt and scorn upon her; and the
matron mourns, forlorn and forsaken, like Hecuba:

Modo maxima rerum,
Tot generis, natisque potens...
Nunc trahor exul, inops.
—Ovid, Metamorphoses. xiii


At first, her government, under the administration of the _dogmatists_,
was an absolute _despotism_. But, as the legislative continued to show
traces of the ancient barbaric rule, her empire gradually broke up, and
intestine wars introduced the reign of _anarchy;_ while the _sceptics_,
like nomadic tribes, who hate a permanent habitation and settled mode
of living, attacked from time to time those who had organized
themselves into civil communities. But their number was, very happily,
small; and thus they could not entirely put a stop to the exertions of
those who persisted in raising new edifices, although on no settled or
uniform plan. In recent times the hope dawned upon us of seeing those
disputes settled, and the legitimacy of her claims established by a
kind of _physiology_ of the human understanding—that of the celebrated
Locke. But it was found that—although it was affirmed that this
so-called queen could not refer her descent to any higher source than
that of common experience, a circumstance which necessarily brought
suspicion on her claims—as this _genealogy_ was incorrect, she
persisted in the advancement of her claims to sovereignty. Thus
metaphysics necessarily fell back into the antiquated and rotten
constitution of _dogmatism_, and again became obnoxious to the contempt
from which efforts had been made to save it. At present, as all
methods, according to the general persuasion, have been tried in vain,
there reigns nought but weariness and complete _indifferentism_—the
mother of chaos and night in the scientific world, but at the same time
the source of, or at least the prelude to, the re-creation and
reinstallation of a science, when it has fallen into confusion,
obscurity, and disuse from ill directed effort.

For it is in reality vain to profess _indifference_ in regard to such
inquiries, the object of which cannot be indifferent to humanity.
Besides, these pretended _indifferentists_, however much they may try
to disguise themselves by the assumption of a popular style and by
changes on the language of the schools, unavoidably fall into
metaphysical declarations and propositions, which they profess to
regard with so much contempt. At the same time, this indifference,
which has arisen in the world of science, and which relates to that
kind of knowledge which we should wish to see destroyed the last, is a
phenomenon that well deserves our attention and reflection. It is
plainly not the effect of the levity, but of the matured _judgement_[1]
of the age, which refuses to be any longer entertained with illusory
knowledge, It is, in fact, a call to reason, again to undertake the
most laborious of all tasks—that of self-examination, and to establish
a tribunal, which may secure it in its well-grounded claims, while it
pronounces against all baseless assumptions and pretensions, not in an
arbitrary manner, but according to its own eternal and unchangeable
laws. This tribunal is nothing less than the _Critical Investigation of
Pure Reason_.
"""

tokenizer = AutoTokenizer.from_pretrained("pszemraj/pegasus-x-large-book-summary")
model = AutoModelForSeq2SeqLM.from_pretrained("pszemraj/pegasus-x-large-book-summary")

inputs = tokenizer.encode(text2, return_tensors="pt", truncation=True)

summary_ids = model.generate(inputs)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)
