-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28;
-- gave me info to check interview and bakery_security_log tables
-- theft occured at 10:15 am

SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- thief left bakery one - ten minutes
-- thief withdrew money at the ATM at leggett street
-- Flying the earliest flight tomorrow out of Fiftyville; someone was on the other side of the phone who bought it for them.

SELECT * FROM flights WHERE origin_airport_id = 8 AND day = 29 ORDER BY hour ASC;
-- Gave me the flight_id of the earliest plane flying out of Fiftyville. ALso noticed that the destination airport is airport id 4.
-- airport_id 4 = LGA | LaGuardia Airport | New York City |
-- Now we know the city the theif is fleeing to is New York City

SELECT passport_number FROM passengers WHERE flight_id = 36
-- Gave me list of passports on the earliest flight out of Fiftyville.
-- EVERYONE here is a suspect. We will need to use license plate number and atm withdraws to narrow it down.

SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28;
-- found potential suspects who left between 10:15 - 10:25 and checked their license plates in bakery

SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";
-- Check only withdraws

-- Go down the list of passengers and check individually if they are clear or not.
-- 1. 953679 | Doris | (066) 555-9701 | 7214083635 | M51FA04 - Clear, license plate not in bakery security table
-- 2. 398010 | Sofia | (130) 555-0289 | 1695452385 | G412CB7 - Clear, no bank account
-- 3. 686048 | Bruce | (367) 555-5533 | 5773159633 | 94KL13X - FOUND, present at all scenes (bakery, phone call, atm, and passenger)

-- Accomplice must be the one who revieved Bruce's calls. Track his call record to find accomplice's number.
SELECT * FROM phone_calls WHERE caller = "(367) 555-5533" AND day = 28;
-- We know from witnesses that the call lasted less than a minute. Only option left is therefore the number (375) 555-8161.

-- Search person's name based off this number.
SELECT name FROM people WHERE phone_number = "(375) 555-8161";
-- Result is somone named Robin

-- CONCLUSION
-- THIEF = Bruce
-- CITY ESCAPED TO = New York City
-- ACCOMPLICE = Robin