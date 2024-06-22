import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

export default function Index() {
  const navigate = useNavigate();

  const goToCapture = () => {
    navigate("/capture");
  };

  return (
    <div className="bg-black">
      <header className="bg-black text-white sticky top-0 z-10">
        <section className="max-w-4xl mx-auto p-4 items-center">
          <h1 className="text-2xl font-bold"></h1>
        </section>
      </header>

      <main className="min-h-screen max-w-4xl mx-auto w-full bg-black text-white pt-48">
        <div className="relative x-4 y-0">
          <motion.div
            variants={{
              hidden: {
                opacity: 0,
                y: -300,
              },
              visible: {
                opacity: 1,
                y: 0,
              },
              exit: {
                opacity: 0,
                y: -300,
              },
            }}
            initial="hidden"
            animate="visible"
            exit="exit"
            transition={{ duration: 1.5 }}
          >
            <h2 className="text-5xl font-bold text-center font-roboto">
              How this App works
            </h2>
          </motion.div>
          <motion.div
            variants={{
              hidden: {
                opacity: 0,
                x: -1300,
              },
              visible: {
                opacity: 1,
                x: 0,
              },
              exit: {
                opacity: 0,
                x: -1300,
              },
            }}
            initial="hidden"
            animate="visible"
            exit="exit"
            transition={{ duration: 1.5 }}
          >
            <p className="pt-10 gap-3 text-align-left pl-10 pr-10 font-roboto">
              <span className="text-4xl font-bold bg-gradient-to-l from-green-400 to-green-100 bg-clip-text text-transparent">
                Soundtrack of Your Emotion
              </span>
              is a revolutionary app that blends cutting-edge facial recognition
              technology with the power of music to enhance your emotional
              well-being. With a simple snapshot, our app captures your facial
              expression and accurately processes it into one of three distinct
              moods: sad, neutral, or happy. Depending on your detected mood,
              Soundtrack of Your Emotion then curates a personalized Spotify
              playlist to match and elevate your emotional state.
            </p>
          </motion.div>
        </div>
        <motion.div
          variants={{
            hidden: {
              opacity: 0,
              x: 1300,
            },
            visible: {
              opacity: 1,
              x: 0,
            },
            exit: {
              opacity: 0,
              x: 1300,
            },
          }}
          initial="hidden"
          animate="visible"
          exit="exit"
          transition={{ duration: 1.5 }}
        >
          <div className="pt-10 pl-10 pr-10 flex items-center justify-center">
            <button
              className="bg-gradient-to-r from-green-400 to-green-100  transition ease-in-out delay-150  hover:scale-110 hover:bg-white-200 duration-300 px-6 py-2 rounded-full text-black font-roboto"
              onClick={goToCapture}
            >
              Get Started
            </button>
          </div>
        </motion.div>
      </main>

      <footer className="bg-black text-white sticky bottom-0 z-10"></footer>
    </div>
  );
}
