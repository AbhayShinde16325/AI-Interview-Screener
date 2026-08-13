import Modal from '../ui/Modal'
import Button from '../ui/Button'

export default function InterviewExitModal({ open, onContinue, onLeave }) {
  return (
    <Modal
      open={open}
      onClose={onContinue}
      title="Leave interview?"
      footer={
        <>
          <Button variant="secondary" onClick={onContinue}>
            Continue interview
          </Button>
          <Button variant="dangerSolid" onClick={onLeave}>
            Leave interview
          </Button>
        </>
      }
    >
      <p>Your progress may be lost if you leave now.</p>
    </Modal>
  )
}
